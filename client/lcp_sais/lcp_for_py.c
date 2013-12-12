/*
 * suftest.c for sais-lite
 * Copyright (c) 2008-2010 Yuta Mori All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sais.h"

long getSuffixLength(char *fname) {
   FILE* fp;
   long n;
   
   /* Open a file for reading. */
   if((fp = fopen(fname, "rb")) == NULL) {
      fprintf(stderr, "Cannot open file: %s\n", fname);
      perror(NULL);
      exit(EXIT_FAILURE);
   }
   
   if(fseek(fp, 0, SEEK_END) == 0) {
      n = ftell(fp);
      rewind(fp);
      if(n < 0) {
         fprintf(stderr, "Cannot ftell `%s': ", fname);
         perror(NULL);
         exit(EXIT_FAILURE);
      }
   } else {
      fprintf(stderr, "Cannot fseek `%s': ", fname);
      perror(NULL);
      exit(EXIT_FAILURE);
   }
   
   fclose(fp);
   return n;
}

int getSuffixLCPArray(char *fname, int *SA, int *LCP, long n) {
   FILE *fp;
   unsigned char *T;
   
   /* Open a file for reading. */
   if((fp = fopen(fname, "rb")) == NULL) {
      fprintf(stderr, "Cannot open file: %s\n", fname);
      perror(NULL);
      exit(EXIT_FAILURE);
   }

  /* Allocate 9n bytes of memory. */
  T = (unsigned char *)malloc((size_t)n * sizeof(unsigned char));
//  SA = (int *)malloc((size_t)(n+1) * sizeof(int)); // +1 for computing LCP
//  LCP = (int *)malloc((size_t)n * sizeof(int));
  if((T == NULL) || (SA == NULL) || (LCP == NULL)) {
    fprintf(stderr, "Cannot allocate memory.\n");
    exit(EXIT_FAILURE);
  }

  /* Read n bytes of data. */
  if(fread(T, sizeof(unsigned char), (size_t)n, fp) != (size_t)n) {
    fprintf(stderr, "%s",
      (ferror(fp) || !feof(fp)) ? "Cannot read from" : "Unexpected EOF in");
    perror(NULL);
    exit(EXIT_FAILURE);
  }
  fclose(fp);

//if (n < 256) printf("%s\n", T);
//T[n-1]=0;
 /* int ii; */
 /* for (ii=0;ii<n;++ii) printf("%i,", (int)T[ii]); printf("\n");  */
//if (n < 256) printf("%s\n", T);

 //int j;
 /* for (j = 0; j < n; j++) printf("%i,", (int) T[j]); printf("\n"); */
  
  /* Construct the suffix array. */
  //fprintf(stderr, "%s: %ld bytes ... \n", fname, n);
  //start = clock();
  if(sais(T, SA, LCP, (int)n) != 0) {
    fprintf(stderr, "Cannot allocate memory.\n");
    exit(EXIT_FAILURE);
  }
  //finish = clock();
  //fprintf(stderr, "induced: %.4f sec\n", (double)(finish - start) / (double)CLOCKS_PER_SEC);

  /* // check LCP: */
 //  int i,l, j; 
// for (i = 1; i < n; ++i) {
 //    l = 0; 
  //   while (T[SA[i]+l]==T[SA[i-1]+l]) ++l; 
  //   if (l != LCP[i]) { 
  //     printf("Error at position %i\n", i); 
  //     printf("%i vs. %i\n", l, LCP[i]); 
  //     for (j = 0; j < 10; j++) printf("%c", T[SA[i]+j]); printf("\n"); 
  //     for (j = 0; j < 10; j++) printf("%c", T[SA[i-1]+j]); printf("\n"); 
  //     exit(-1); 
  //   } 
  // } 

  // naive LCP:
  //start = clock();
  //int i,l;
  //for (i = 1; i < n; ++i) {
  //  l = 0;
  //  while (T[SA[i]+l]==T[SA[i-1]+l]) ++l;
  //  LCP[i] = l;
  //}
  //finish = clock();
  //fprintf(stderr, "naive: %.4f sec\n", (double)(finish - start) / (double)CLOCKS_PER_SEC);

  /* Deallocate memory. */
  //free(SA);
  //free(LCP);
  free(T);

  return 0;
}
