/* This is the only file you will be editing.
 * - Copyright of Starter Code: Prof. Kevin Andrea, George Mason University.  All Rights Reserved
 * - Copyright of Student Code: You!  
 * - Restrictions on Student Code: Do not post your code on any public site (eg. Github).
 * -- Feel free to post your code on a PRIVATE Github and give interviewers access to it.
 * -- You are liable for the protection of your code from others.
 * - ASCII Art Adapted from Regular Calculator by Jeremy J. Olson
 * -- Original File: https://www.asciiart.eu/electronics/calculators
 * - Date: Jan 2025
 */

/* CS367 Project 2, Fall Semester, 2025
 * Fill in your Name, GNumber, and Section Number in the following comment fields
 * Name: Jakob Elmore
 * GNumber: G01302977
 * Section Number: CS367-007            (Replace the _ with your section number)
 */

/* _____________________
  |  _________________  |
  | |     MUAN    3.25| |
  | |_________________| |
  |  ___ ___ ___   ___  |
  | | 7 | 8 | 9 | | + | |
  | |___|___|___| |___| |
  | | 4 | 5 | 6 | | - | |
  | |___|___|___| |___| |
  | | 1 | 2 | 3 | | x | |
  | |___|___|___| |___| |
  | | . | 0 | = | | V | |
  | |___|___|___| |___| |
  |_____________________|
 */

#include <stdio.h>
#include <stdlib.h>
#include "common_structs.h"
#include "common_definitions.h"
#include "common_functions.h"
#include "smallfp.h"

// Feel free to add many Helper Functions, Consts, and Definitions!

//zeros s exp  frac
//00000 0 0000 000000
//        9876 543210

//0x0540
//00000 1 0101 000000

//NaN
//00000 X 1111 000001 = 0x03C1 for positive NaN (doesnt matter)

//INF
//00000 X 1111 000000 = 0x03C0 for pos inf, 0x07C0 for neg inf

/**
 * - number is the smallfp_s that you want to change
 * - bit is the bit number you want to change counting from the right starting at 0
 * 
*/
int set_bit(smallfp_s number, int bit){
	return number | (1 << bit);
}

/**
 * - number is the smallfp_s that you want to change
 * - bit is the bit number you want to clear counting from the right starting at 0
 * 
*/
int clear_bit(smallfp_s number, int bit){
    return number & (~(1 << bit));
}

/**
 * - number is the smallfp_s that you want to check
 * - bit is the bit number you want to check counting from the right starting at 0
 * 
*/
int check_bit(int number, int bit){
    if (number & (1 << bit)){return 1;}
    else {return 0;}
}

//returns an int with the binary of the short given to it.
//overflow returns 
int whole_to_binary(unsigned short num){
    //handles negative
    if (num < 0){num *= -1;}
    int max_len = 4;
    int binary = 0b0000;

    //coverts to binary by dividing by 2
    int counter = 0;
    while (counter < max_len){
        if (num % 2 == 1){
            binary |= 1 << counter;
            num -= 1;
        }
        else{
            binary |= 0 << counter;
        }
        counter ++;
        num /= 2;
    }

    return binary;
}

int get_exp(smallfp_s value){
    int exp = 0b0000;
    for (int i = 0; i < 4; i ++){
        if (check_bit(value, 6 + i) == 1){
            exp = set_bit(exp, i);
        }
    }
    return exp;
}

int get_frac(smallfp_s value){
    int frac = 0b000000;
    for (int i = 0; i < 6; i ++){
        if (check_bit(value, i) == 1){
            frac = set_bit(frac, i);
        }
    }
    return frac;
}

/**
 * Turns places whole_num into frac and returns the exp
 */
int normalize(int whole_num, unsigned short * frac){
    int lsb;
    int counter = 0;
    while (whole_num > 1){
        counter ++;
        lsb = whole_num & 1;
        whole_num = whole_num >> 1;
        * frac = * frac >> 1;
        * frac |= (lsb << (15)); // sets first bit to the bit that got moved off when shifting whole_num right
    }
    return counter;
}

/**
 * Takes the whole num out of frac and returns the whole num as binary
 */
int denormalize(int exp, int * frac){
    int msb;
    int whole_num = 0b0001; //default value assumes starting with 1
    while(exp > 0){
        msb = check_bit(* frac, 5);
        whole_num = whole_num << 1;
        if (msb == 1){
            whole_num = set_bit(whole_num, 0);
            * frac = clear_bit(* frac, 5);
        }
        * frac = * frac << 1;
        exp --;
    }

    * frac = * frac << 10; //frac is stored in smallfp_s as 6 bits, but as 16 bits as an int, so has to be moved 10

    return whole_num;
}

// ----------Public API Functions (write these!)-------------------

/* toSmallFP - Converts a Number Struct (whole and fraction parts) into a SmallFP Value
 *  - number is managed by MUAN, DO NOT FREE number.
 *    - You may change the contents of number, but do not free it.
 *  - Follow the project documentation for this function.
 * Return the SmallFP Value or any legal SmallFP NaN representation if number is NULL.
 */
smallfp_s toSmallFP(Number_s *number) {
	if (number == NULL){return 0x03C1;}// checks for valid args. returns nan if null

	smallfp_s return_num = 0x0000;
	smallfp_s * return_ptr = &return_num;

    //printf("fraction initial value 0x%x\n", number->fraction);

	//checks for nan
	if (number->is_nan == 1){
		return_num = 0x3C1;
		return return_num;
	}

	//checks for inf
	//returns pos or neg inf 
	//(idk if this matters)
	if (number->is_infinity == 1){
		if (number->is_negative == 1){
			return_num = 0x03C0;
		}
		else{
			return_num = 0x07C0;
		}
		return return_num;
	}

	//sets bits when needed
    if (number->is_negative == 1){
	    return_num = set_bit(return_num, 10);
    }

    //converts whole to binary representation
    int whole = whole_to_binary(number->whole);

    int e = normalize(whole, &number->fraction);

    int bias = 7;
    char exp = whole_to_binary(bias + e);

    //setting exp
    int counter = 0;
    while (counter < 4){
        if (check_bit(exp, counter) == 1){
            return_num = set_bit(return_num, (6 + counter));
        }
        counter ++;
    }

    //setting frac
    counter = 0;
    while (counter < 6){
        if ((check_bit(number->fraction, 16 - counter)) == 1){
            return_num = set_bit(return_num, 6 - counter);
        }
        counter ++;
    }
    
    return return_num;
}

/* toNumber - Converts a SmallFP Value into a Number Struct (whole and fraction parts)
 *  - number is managed by MUAN, DO NOT FREE or re-Allocate number.
 *    - It is already allocated.  Do not call malloc/calloc for number.
 *  - Follow the project documentation for this function.
 *  If the conversion is successful, return 0. 
 *  - If number is NULL, return -1.
 */
int toNumber(Number_s * number, smallfp_s value) {
	if (number == NULL){return -1;}// checks for valid args

    if (check_bit(value, 10) == 1){
        number->is_negative = 1;
    }

    //checking for nan and inf
    int all_ones = 1;
    for (int i = 6; i <= 9; i ++){
        if (check_bit(value, i) == 0){
            all_ones = 0;
            break;
        }
    }

    //determine if nan or inf
    if (all_ones == 1){
        int is_inf = 0;
        for (int i = 0; i < 6; i ++){
            if (check_bit(value, i) == 1){
                is_inf = 0;
                break;
            }
        }

        if (is_inf == 1){
            number->is_infinity = 1;
            number->is_nan = 0;
        }
        else{
            number->is_nan = 1;
            number->is_infinity = 0;
        }
    }
    else{
        number->is_nan = 0;
        number->is_infinity = 0;
    }

    //find exp and frac 
    int bias = 7;
    int exp = get_exp(value) - bias;
    int frac = get_frac(value);
    //printf("before frac = 0x%x, exp = %d\n", frac, exp);

    int whole = denormalize(exp, &frac);

    //printf("after frac = 0x%x\n", frac);

    number->whole = whole;
    number->fraction = frac;

    return 0; //success
}


int binary_to_mult_int(smallfp_s val){
    //easy way to grab the whole number from val instead of messing around with the exp
    Number_s * temp_num = (Number_s *)malloc(sizeof(Number_s));
    toNumber(temp_num, val);

    int binary_val = whole_to_binary(binary_val);

    int msb;
    for (int i = 0; i < 6; i ++){
        msb = check_bit(temp_num->fraction, 5);
        binary_val = binary_val << 1;
        if (msb == 1){
            binary_val = set_bit(binary_val, 0);
            temp_num->fraction = clear_bit(temp_num->fraction, 5);
        }
        temp_num->fraction = temp_num->fraction << 1;
    }

    free(temp_num);
    return binary_val;
}

int get_e(smallfp_s val){
    int exp = 0b0000;
    int bias = 7;
    for (int i = 0; i < 4; i ++){
        if (check_bit(val, 6 + i)){
            exp = set_bit(exp, i);
        }
    }
    return exp - bias;
}

int get_m(smallfp_s val){
    int m = 0b1000000;
    for (int i = 0; i < 6; i ++){
        if (check_bit(val, i) == 1){
            m = set_bit(m, i);
        }
    }
    // printf("returning m = %x\n", m);
    return m;
}


/* mulSmallFP - Performs an operation on two SmallFP values
 *  - Follow the project documentation for this function.
 * Return the resulting smallfp_s value
 */
smallfp_s mulSmallFP(smallfp_s val1, smallfp_s val2) {
    //adds the frac value to the end of the whole num in binary, moved over 6 spaces each

    //check and remove sign bit
    int sign = check_bit(val1, 10) ^ check_bit(val2, 10);
    int bias = 7;
    
    val1 = clear_bit(val1, 10);
    val2 = clear_bit(val2, 10);

    int return_val = 0b000000000000;

    int e_1 = get_e(val1);
    int e_2 = get_e(val2);

    int m_1 = get_m(val1);
    int m_2 = get_m(val2);

    int prod_e = e_1 + e_2 + bias;
    int prod_m = m_1 * m_2;

    //sets negative
    if (sign == 1){
        return_val = set_bit(return_val, 10);
    }

    //underflow, return 0 value
    if (prod_e <= 0 && 1 <= prod_m && prod_m < 2){
        return return_val;
    }

    //overflow, return inf (X 1111 000000)
    if (prod_e >= 15){
        for (int i = 0; i < 4; i ++){
            return_val = set_bit(return_val, 6 + i);
        }
        return return_val;
    }


    int offset = 12;
    for (int i = 0; i < 6; i ++){
        if (check_bit(prod_m, offset - i) == 1){
            return_val = set_bit(return_val, 6 - i); //reverses it
        }
    }

    for (int i = 0; i < 4; i ++){
        if (check_bit(prod_e, i) == 1){
            return_val = set_bit(return_val, 6 + i);
        }
    }
  	return return_val;
}

/* addSmallFP - Performs an operation on two SmallFP values
 *  - Follow the project documentation for this function.
 * Return the resulting smallfp_s value
 */
smallfp_s addSmallFP(smallfp_s val1, smallfp_s val2) {
    int e_val1 = get_e(val1);
    int e_val2 = get_e(val2);

    int m_val1 = get_m(val1);
    int m_val2 = get_m(val2);

    int e_diff = e_val1 - e_val2;

    while (e_diff > 2){
        m_val2 = m_val2 << 1;
        e_val2 -= 1;
        e_diff = e_val1 - e_val2;
    }

    while(e_diff < 0){
        m_val1 = m_val1 >> 1;
        e_val1 += 1;
        e_diff = e_val1 - e_val2;
    }

    int sum = m_val1 + m_val2;
    int frac = 0b000000;
    int * frac_p = &frac;

    e_val1 += normalize(sum, frac_p);

    

  	return 0;
}

/* opSmallFP - Performs an operation on two SmallFP values
 *  - Follow the project documentation for this function.
 * Return the resulting smallfp_s value
 */
smallfp_s subSmallFP(smallfp_s val1, smallfp_s val2) {
    //change the signs of one of the values then add it

    val2 = negSmallFP(val2);

  	return addSmallFP(val1, val2);
}

/* negSmallFP - Negates a SmallFP Value.
 *  - Follow the project documentation for this function.
 * Return the resulting SmallFP Value
 */
smallfp_s negSmallFP(smallfp_s value) {
    return value ^= (1 << (10)); //swaps the sign bit
}

// int main(){
//     Number_s number;
//     number.whole = 3;
//     number.fraction = 0.25;

//     printf("number = %d%f", number.whole, number.fraction);

//     return 0;
// }