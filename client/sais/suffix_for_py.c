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

int getSuffixArray(char *fname, int *SA, long n) {
  FILE *fp;
  unsigned char *T;

  /* Open a file for reading. */
  if((fp = fopen(fname, "rb")) == NULL) {
    fprintf(stderr, "Cannot open file: %s\n", fname);
    perror(NULL);
    exit(EXIT_FAILURE);
  }

  /* Allocate 5n bytes of memory. */
  T = (unsigned char *)malloc((size_t)n * sizeof(unsigned char));
  if((T == NULL) || (SA == NULL)) {
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

  /* Construct the suffix array. */
  if(sais(T, SA, (int)n) != 0) {
    fprintf(stderr, "Cannot allocate memory.\n");
    exit(EXIT_FAILURE);
  }

  /* Deallocate memory. */
  free(T);

  return 0;
}
