#include <stdio.h>
#include <threads.h>
#include <unistd.h>
#include <stdatomic.h>

atomic_int x ;

int counter = 1 ;
int running = 1 ;

int incre(void *args) {
  while(running) {
    atomic_store(&x, counter) ;
    counter++ ;
    usleep(20) ;
  }
  thrd_exit(10) ;
}

int print(void *args) {
  int temp ;
  while(running) {
    temp = atomic_exchange(&x, 0) ;
    if(temp) {
      printf("%d\n", temp) ;
    }
  }
  thrd_exit(10) ;
}

int main() {
  thrd_t try1 ;
  thrd_t try2 ;
  int result ;
  // atomic_init(&x, 215) ;
  thrd_create(&try1, incre, NULL) ;
  thrd_create(&try2, print, NULL) ;
  usleep(100000) ;
  running = 0 ;
  // thrd_join(try, &result) ;
  // while(1) ;
  // sleep(1) ;
  // printf("%d\n", result);
  return 0 ;
}
   