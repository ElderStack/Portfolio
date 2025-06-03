/* This is the only file you will be editing.
 * - wlf_sched.c (Wlf Scheduler Library Code)
 * - Copyright of Starter Code: Prof. Kevin Andrea, George Mason University. All Rights Reserved
 * - Copyright of Student Code: You!  
 * - Copyright of ASCII Art: Modified from an uncredited author's work:
 * -- https://www.asciiart.eu/animals/wolves
 * - Restrictions on Student Code: Do not post your code on any public site (eg. Github).
 * -- Feel free to post your code on a PRIVATE Github and give interviewers access to it.
 * -- You are liable for the protection of your code from others.
 * - Date: Jan 2025
 */

/* CS367 Project 1, Spring Semester, 2025
 * Fill in your Name, GNumber, and Section Number in the following comment fields
 * Name: Jakob Elmore 
 * GNumber:  G01302977
 * Section Number: CS367-002             (Replace the _ with your section number)
 */

/* wlf CPU Scheduling Library
                     .
                    / V\
                  / `  /
                 <<   |
                 /    |
               /      |
             /        |
           /    \  \ /
          (      ) | |
  ________|   _/_  | |
<__________\______)\__)
*/
 
/* Standard Library Includes */
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
/* Unix System Includes */
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <pthread.h>
#include <sched.h>
/* DO NOT CHANGE THE FOLLOWING INCLUDES - Local Includes 
 * If you change these, it will not build on Zeus with the Makefile
 * If you change these, it will not run in the grader
 */
#include "wlf_sched.h"
#include "strawhat_scheduler.h"
#include "strawhat_support.h"
#include "strawhat_process.h"
/* DO NOT CHANGE ABOVE INCLUDES - Local Includes */

/* Feel free to create any definitions or constants you like! */

/* Feel free to create any helper functions you like! */

/*** Wlf Library API Functions to Complete ***/

/* Initializes the Wlf_schedule_s Struct and all of the Wlf_queue_s Structs
 * Follow the project documentation for this function.
 * Returns a pointer to the new Wlf_schedule_s or NULL on any error.
 * - Hint: What does malloc return on an error?
 */

Wlf_schedule_s *wlf_initialize() {
    Wlf_schedule_s * wlf_ptr = (Wlf_schedule_s *)malloc(sizeof(Wlf_schedule_s));
    if (wlf_ptr == NULL){
        return NULL;
    }

    wlf_ptr->ready_queue_high = (Wlf_queue_s *)malloc(sizeof(Wlf_queue_s));
    wlf_ptr->ready_queue_normal = (Wlf_queue_s *)malloc(sizeof(Wlf_queue_s));
    wlf_ptr->terminated_queue = (Wlf_queue_s *)malloc(sizeof(Wlf_queue_s));

    if (wlf_ptr->ready_queue_high == NULL || wlf_ptr->ready_queue_normal == NULL || wlf_ptr->terminated_queue == NULL){
        return NULL;
    }

    wlf_ptr->ready_queue_high->count = 0;
    wlf_ptr->ready_queue_high->head = NULL;
    wlf_ptr->ready_queue_high->tail = NULL;

    wlf_ptr->ready_queue_normal->count = 0;
    wlf_ptr->ready_queue_normal->head = NULL;
    wlf_ptr->ready_queue_normal->tail = NULL;

    wlf_ptr->terminated_queue->count = 0;
    wlf_ptr->terminated_queue->head = NULL;
    wlf_ptr->terminated_queue->tail = NULL;

    return wlf_ptr;
}
/* Allocate and Initialize a new Wlf_process_s with the given information.
 * - Malloc and copy the command string, don't just assign it!
 * Follow the project documentation for this function.
 * - You may assume all arguments within data are Legal and Correct for this Function Only
 * Returns a pointer to the Wlf_process_s on success or a NULL on any error.
 */
Wlf_process_s *wlf_create(Wlf_create_data_s *data) {
    //printf("create start\n");
    Wlf_process_s * wlf_ptr = (Wlf_process_s *)malloc(sizeof(Wlf_process_s));
    if (wlf_ptr == NULL){
        return NULL;
    }

    /*
    bits 0-7 are the exit code
    bit 11 is the high priority flag
    bit 12 is the critical flag
    bits 13-15 represent state of the process: ready, running, then terminated

    default - no critical or high priority = 100 00 000 00000000 = 0x8000
    default - critical = 100 11 000 00000000 = 0xA800
    default - high = 100 01 000 00000000 = 0x8800
    */

    if (data->is_critical == 1){
      wlf_ptr->state = 0xA800;
    }
    else if (data->is_high == 1){
      wlf_ptr->state = 0x8800;
    }
    else{
      wlf_ptr->state = 0x8000;
    }   

    wlf_ptr->age = 0;
    wlf_ptr->pid = data->pid;
    wlf_ptr->cmd = (char *)malloc(sizeof(char) * 50);

    if (wlf_ptr->cmd == NULL){
      return NULL;
    }

    int counter = strlen(data->original_cmd);
    strncpy(wlf_ptr->cmd, data->original_cmd, counter);

    wlf_ptr->next = NULL;

    //printf("create end\n");
    return wlf_ptr;
}


//return 1 if bit_num in num is 1
int check_bit(int num, int bit_num){
    //printf("check bit func\n");
    return 1 & num >> (bit_num - 1);
}

//adds process to the end of a queue
//return 0 on success, -1 on failure
int append_to_queue(Wlf_queue_s * queue, Wlf_process_s * process){
    //printf("append start\n");
    if (queue == NULL || process == NULL){
        return -1;
    }

    if (queue->head == NULL){
        queue->head = process;
        //printf("append head end\n");
        return 0;
    }

    Wlf_process_s * iterator = queue->head;
    if (iterator != NULL){
        while(iterator->next != NULL){
            iterator=iterator->next;
        }
    }
    
    iterator->next = process;
    queue->count += 1;
    //printf("append end\n");
    return 0;
}

/* Inserts a process into the appropriate Ready Queue (singly linked list).
 * Follow the project documentation for this function.
 * - Do not create a new process to insert, insert the SAME process passed in.
 * Returns a 0 on success or a -1 on any error.
 */
int wlf_enqueue(Wlf_schedule_s *schedule, Wlf_process_s *process) {
    //printf("enqueue start\n");
    if (schedule == NULL || process == NULL){
        return -1;
    }

    //sets ready state
    process->state ^= 0x8000;

    if (check_bit(process->state, 12) == 1 || check_bit(process->state, 11) == 1){
        //printf("enqueue ready end\n");
        return append_to_queue(schedule->ready_queue_high, process);
    }
    else{
        //printf("enqueue normal end\n");
        return append_to_queue(schedule->ready_queue_normal, process);
    }
}

/* Returns the number of items in a given Wlf Queue (singly linked list).
 * Follow the project documentation for this function.
 * Returns the number of processes in the list or -1 on any errors.
 */
int wlf_count(Wlf_queue_s *queue) {
    //printf("count start\n");
    if (queue == NULL){
        return -1;
    }
    //printf("count end\n");
    return queue->count;
}

/* Selects the best process to run from the Ready Queues (singly linked list).
 * Follow the project documentation for this function.
 * Returns a pointer to the process selected or NULL if none available or on any errors.
 * - Do not create a new process to return, return a pointer to the SAME process selected.
 * - Return NULL if the ready queues were both empty OR if there were any errors.
 */
Wlf_process_s *wlf_select(Wlf_schedule_s *schedule) {
    //printf("select start\n");
    if (schedule == NULL || (schedule->ready_queue_high == NULL && schedule->ready_queue_normal == NULL)){
        return NULL;
    }

    Wlf_process_s * iterator;
    Wlf_process_s * return_process;

    if (schedule->ready_queue_high->head != NULL){
        iterator = schedule->ready_queue_high->head;

        while(iterator->next){
            if (check_bit(iterator->state, 12) == 1){
                return_process = iterator;
                break;
            }
        iterator=iterator->next;
        }

        return_process = schedule->ready_queue_high->head;
        schedule->ready_queue_high->head = schedule->ready_queue_high->head->next;
    }

    else if (schedule->ready_queue_normal->head != NULL){
        return_process = schedule->ready_queue_normal->head;
        schedule->ready_queue_normal->head = schedule->ready_queue_normal->head->next;
    }
    else{
        return NULL;
    }

    return_process->age = 0;
    //bit 13 needs to be 0, bit 14 needs to be 1

    return_process->state ^= 0xC000;
    return_process->next = NULL;
    //printf("select end\n");
    return return_process;
}

/* Ages all Process nodes in the Ready Queue - Normal and Promotes any that are Starving.
 * If the Ready Queue - Normal is empty, return 0.  (Success if nothing to do)
 * Follow the specification for this function.
 * Returns a 0 on success or a -1 on any error.
 */
int wlf_promote(Wlf_schedule_s *schedule) {
    //printf("promote start\n");
    if (schedule == NULL || schedule->ready_queue_normal == NULL){
        return -1;
    }

    Wlf_process_s * iterator = schedule->ready_queue_normal->head;
    Wlf_process_s * lag_iterator = iterator;
    while (iterator != NULL){
        if (iterator->age >= STARVING_AGE){
            lag_iterator->next = iterator->next;
            iterator->next = NULL;
            append_to_queue(schedule->ready_queue_high, iterator);
        }
        lag_iterator = iterator;
        iterator = iterator->next;
    }

    //printf("promote end\n");
    return 0;
}

/* This is called when a process exits normally that was just Running.
 * Put the given node into the Terminated Queue and set the Exit Code 
 * - Do not create a new process to insert, insert the SAME process passed in.
 * Follow the project documentation for this function.
 * Returns a 0 on success or a -1 on any error.
 */
int wlf_exited(Wlf_schedule_s *schedule, Wlf_process_s *process, int exit_code) {
    //printf("exit start\n");
    if (schedule == NULL || process == NULL){
        return -1;
    }

    process->state ^= 0x6000; // changes state from running to terminated

    process->state = (process->state & ~0x000F) | (exit_code & 0x000F);

    append_to_queue(schedule->terminated_queue, process);

    //printf("exit end\n");
    return 0;
}

/* This is called when the OS terminates a process early. 
 * - This will either be in your Ready Queue - High or Ready Queue - Normal.
 * - The difference with wlf_exited is that this process is in one of your Queues already.
 * Remove the process with matching pid from either Ready Queue and add the Exit Code to it.
 * - You have to check both since it could be in either queue.
 * Follow the project documentation for this function.
 * Returns a 0 on success or a -1 on any error.
 */
int wlf_killed(Wlf_schedule_s *schedule, pid_t pid, int exit_code) {
    //printf("killed start\n");
    if (schedule == NULL){
        return -1;
    }

    Wlf_process_s * iterator = schedule->ready_queue_high->head;
    Wlf_process_s * lag_iterator = iterator;
    int found = 0;

    //checking high priority
    while (iterator != NULL){
        if (iterator->pid == pid){
            found = 1;
            lag_iterator->next = iterator->next;
            iterator->next = NULL;
            break;
        }
        lag_iterator = iterator;
        iterator = iterator->next;
    }

    //checking normal priority
    if (found != 1){
        iterator = schedule->ready_queue_normal->head;
        lag_iterator = iterator;

        while (iterator != NULL){
        if (iterator->pid == pid){
            found = 1;
            lag_iterator->next = iterator->next;
            iterator->next = NULL;
            break;
        }
        lag_iterator = iterator;
        iterator = iterator->next;
        }
    }

    if (found != 1){
        return -1;
    }

    iterator->state ^= 0x6000;
    iterator->state = (iterator->state & ~0x00FF) | (exit_code & 0x00FF);

    //printf("killed end\n");
    return 0;
}

/* This is called when StrawHat reaps a Terminated (Defunct) Process.  (reap command).
 * Remove and free the process with matching pid from the Termainated Queue.
 * Follow the specification for this function.
 * Returns the exit_code on success or a -1 on any error (such as process not found).
 */
int wlf_reap(Wlf_schedule_s *schedule, pid_t pid) {
    //printf("reap start\n");
    if (schedule == NULL || schedule->terminated_queue == NULL){
        return -1;
    }

    Wlf_process_s * iterator = schedule->terminated_queue->head;
    Wlf_process_s * lag_iterator = iterator;
    int found = 0;

    //if have to check each pid
    if (pid != 0){
        //checking terminated
        while (iterator != NULL){
            if (iterator->pid == pid){
                lag_iterator->next = iterator->next;
                iterator->next = NULL;
                found = 1;
                break;
            }
            lag_iterator = iterator;
            iterator = iterator->next;
        }
    }

    //if head is to be removed
    else{
        schedule->terminated_queue->head = iterator->next;
        found = 1;
    }

    if (found != 1){
        return -1;
    }

    int exit_code = iterator->state & 0xFF;

    free(iterator->cmd);
    free(iterator->next);
    free(iterator);

    //printf("reap end\n");
    return exit_code;
}

/* Gets the exit code from a terminated process.
 * (All Linux exit codes are between 0 and 255)
 * Follow the project documentation for this function.
 * Returns the exit code if the process is terminated.
 * If the process is not terminated, return -1.
 */
int wlf_get_ec(Wlf_process_s *process) {
    //printf("code start\n");
    if (process == NULL){
        return -1;
    }

    if (check_bit(process->state, 15) == 1){
        //printf("code end\n");
        return process->state & 0x00FF;
    }
    return -1;
}

void free_queue(Wlf_queue_s * queue){
    //printf("free start\n");
    if (queue == NULL){
        return;
    }

    Wlf_process_s * lag_iterator = queue->head;
    if (lag_iterator != NULL){
        Wlf_process_s * iterator = lag_iterator->next;
        
        while (iterator != NULL){
            free(lag_iterator->cmd);
            free(lag_iterator->next);
            free(lag_iterator);
            lag_iterator = iterator;
            iterator = iterator->next;
        }
        free(lag_iterator);
        free(iterator);
    }
    else{
        free(queue);
    }
    //printf("free end\n");
}

/* Frees all allocated memory in the Wlf_schedule_s, all of the Queues, and all of their Nodes.
 * Follow the project documentation for this function.
 * Returns void.
 */
void wlf_cleanup(Wlf_schedule_s *schedule) {
    //printf("cleanup start\n");
    if (schedule == NULL){
        free(schedule);
        return;
    }

    //printf("free queues running\n");
    free_queue(schedule->ready_queue_high);
    free_queue(schedule->ready_queue_normal);
    free_queue(schedule->terminated_queue);
    free(schedule);
    //printf("cleanup end\n");
}
