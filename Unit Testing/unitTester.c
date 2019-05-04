/*
 * Unit testing framework for Cal Poly Hyperloop adapted by one writen
 *    for CPE 357 by Kurt Mammen
 */

/*
 * Usage: unitTester [functionName | -special functionName]
 *
 * When no option is specified ALL of the regular tests are run.
 * When "functionName" is specified that single regular test is run.
 * When "-special functionName" is specified that single special test is run.
 *    
 * To add a new test you must:
 * 
 *    1) Write a test function.
 *    2) Add its name to the appropriate array of test functions, core for tests you want to run every time
 *          feature for tests you only want to run individualy
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#include <float.h>
#include "unitTest.h"

// --------------------------------------------------------------------------------------
// Include the file/s you are testing here:
// --------------------------------------------------------------------------------------



// --------------------------------------------------------------------------------------
//    housekeeping functions
// --------------------------------------------------------------------------------------

#define TEST_ALL -1
#define REGULAR -2 
#define SPECIAL -3

/* Prototype for all test functions. This allows the creation of an array of
 * function pointers which makes the testing code shorter and more clear. It
 * also makes it easier/faster to add new tests - NICE!
 */
typedef void (*TestFunc)();

/* Structure for a test. See initRegularTests and initSpecialTests to see
 * how it is used.
 */
typedef struct
{
   TestFunc fn;
   char *fnName;
} Test;

// --------------------------------------------------------------------------------------
//    write tests in this section
// --------------------------------------------------------------------------------------

// Use helper functions if you want
void functionThatShouldThrowError()
{
   exit(EXIT_FAILURE);
}

/* 
 * EXAMPLE CORE TEST: follow this format
 */
static void core00()
{
   // Initialize variables you need and do computations
   float f1 = -1.05;
   float f2 = -1.05;

   unsigned long ul1 = 2923874;
   unsigned long ul2 = 2923874;

   double d1 = 2.0001;
   double d2 = 2;
   double epsilon = .001;

   int b1 = 1;
   int b2 = 1;

   char c1 = 'a';
   char c2 = 'a';

   char* s1 = "bannana";
   char* s2 = "bannana";
   
   // Use one or more of the test macros to ensure correct values:
   TEST_SIGNED(f1, f2);
   TEST_UNSIGNED(ul1, ul2);
   TEST_REAL(d1, d2, epsilon);
   TEST_BOOLEAN(b1, b2);
   TEST_CHAR(c1, c2);
   TEST_STRING(s1, s2);
   TEST_ERROR(functionThatShouldThrowError());
}

/* 
 * EXAMPLE FEATURE TEST: follow this format
 */
static void feature00()
{ 
   // Use the same format at a core test
   int b1 = 1;
   int b2 = 1;

   TEST_BOOLEAN(b1, b2);
}

// --------------------------------------------------------------------------------------
//       Infrastucture to run the tests
// --------------------------------------------------------------------------------------


static void testAll(Test* tests)
{
   int i;

   for (i = 0; tests[i].fn != NULL; i++)
   {
      printf("Running regular %s\n", tests[i].fnName);

      /* Call the test function via function pointer in the array */
      tests[i].fn();
   }
}

static void findAndCall(Test* tests, const char *type, char *fnName)
{
   int i;

   for (i = 0; tests[i].fn != NULL; i++)
   {
      if (0 == strcmp(tests[i].fnName, fnName))
      {
         /* Found it, call the function via function pointer... */
         printf("Running %s %s\n", type, fnName);
         tests[i].fn();
         return;
      }
   }

   fprintf(stderr, "ERROR %s %s: Function not found\n", type, fnName);
   exit(EXIT_FAILURE);
}

static void runTests(Test *tests, const char *type, char *fnName)
{
   if (fnName == NULL)
      testAll(tests);
   else
      findAndCall(tests, type, fnName);

   /* Free the tests (allocated in initTests) */
   free(tests);
}

static char* checkArgs(int argc, char *argv[], int *testType)
{
   char *testName;

   if (argc == 1)
   {
      *testType = REGULAR;      
      testName = NULL;
   }
   else if (argc == 2)
   {
      *testType = REGULAR; 
      testName = argv[1];
   }
   else if (argc == 3)
   {
      if (0 != strcmp(argv[1], "-special"))
      {
         fprintf(stderr, "Invalid option '%s'\n", argv[1]);
         exit(EXIT_FAILURE);
      }
      
      *testType = SPECIAL;
      testName = argv[2];
   }
   else
   {
      fprintf(stderr, "Usage: %s [testName | -special testName]\n", argv[0]);
      exit(EXIT_FAILURE);
   }

   return testName;
}

Test* initTests(Test tests[], int size)
{
   Test *dynamicMemory = malloc(size);

   if (dynamicMemory == NULL)
   {
      fprintf(stderr, "FAILURE in %s at %d: ", __FILE__, __LINE__);
      perror(NULL);
      exit(EXIT_FAILURE);
   }

   return memcpy(dynamicMemory, tests, size);
}

// --------------------------------------------------------------------------------------
//       IMPORTANT: YOU MUST ADD YOUR TEST FUNCTIONS TO ONE OF THESE ARRAYS OR THEY WILL
//          NOT RUN!
// --------------------------------------------------------------------------------------

/* Allocates, initializes, and returns the array of regular test functions.
 * Regular test functions are those that are expected to pass or report failure
 * BUT NOT terminate the test driver.
 *
 * By default, the test driver runs ALL of the regular tests. Alternatively, you
 * can run one at a time by simply specifying its name when you invoke the
 * test driver.
 *
 * See initSpecialTests for tests that you always want to run individually.
 *
 * NOTE: The last structure in the array must have NULL values as this indicates
 *    the array's end.
 */
Test* initRegularTests()
{
   Test local[] = {
      {feature00, "feature00"},
      {NULL, NULL}
   };

   /* See IMPORTANT SUBTLETY above regarding the use of sizeof on arrays */
   return initTests(local, sizeof(local));
}

/* Allocates, initializes, and returns the array of special test functions.
 * Special test functions are those that you want to run individually for one
 * reason or another. For example, a test to see if a function asserts failure
 * when it is supposed to.
 *
 * See initRegularTests for tests that can run together.
 *
 * NOTE: The last structure in the array must have NULL values as this indicates
 *    the array's end.
 *
 * IMPORTANT SUBTLETY: You can only use sizeof to obtain an array's size in
 *    the scope where the array is declared, otherwise you will just get
 *    the size of the pointer to the array.
 */
Test* initSpecialTests()
{
   Test local[] = {
      {core00, "core00"},
      {NULL, NULL}
   };

   /* See IMPORTANT SUBTLETY above regarding the use of sizeof on arrays */
   return initTests(local, sizeof(local)); 
}

// --------------------------------------------------------------------------------------
//       Main
// --------------------------------------------------------------------------------------

/*
 * Usage: unitTester [functionName | -special functionName]
 *
 * When no option is specified ALL of the regular tests are run.
 * When "functionName" is specified that single regular test is run.
 * When "-special functionName" is specified that single special test is run.
 *    
 * To add a new test you must:
 * 
 *    1) Write a test function.
 *    2) Add its name to the appropriate array of test functions, core for tests you want to run every time
 *          feature for tests you only want to run individualy
 */
int main(int argc, char *argv[])
{
   char *testName;
   int testType;

   /* Random numbers used to produce "interesting" strings for testing */
   srand(182955);

   /* Make stdout unbuffered so that test output is synchronous on signals */
   setbuf(stdout, NULL);

   /* Get the test name type */
   testName = checkArgs(argc, argv, &testType);
 
   /* Run the test(s)... */
   if (testType == REGULAR)
      runTests(initRegularTests(), "regular", testName);
   else
      runTests(initSpecialTests(), "special", testName);
   
   return 0;
}
