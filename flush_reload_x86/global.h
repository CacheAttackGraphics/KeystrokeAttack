#ifndef _GLOBAL_H_
#define _GLOBAL_H_

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
// #include <cstdint>

typedef uint8_t LOG_ENTRY;

#define PAGE_SIZE 4096

#if INTPTR_MAX == INT32_MAX
    #define ENVIRONMENT_32_BIT
    #define SYSTEM_BITS 32
#elif INTPTR_MAX == INT64_MAX
    #define ENVIRONMENT_64_BIT
    #define SYSTEM_BITS 64
#endif

#ifdef ENVIRONMENT_32_BIT
typedef uint32_t MEM_ADDR;
typedef uint32_t REGISTER;
#define MEM_ADDR_SIZE 4
#else
typedef uint64_t MEM_ADDR;
typedef uint64_t REGISTER;
#define MEM_ADDR_SIZE 8
#endif

#define MEM_ADDR_VALUE(X) *((MEM_ADDR*)X)

#define CACHE_LINE_SIZE 64

#endif
