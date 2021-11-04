//
// Created by akif on 31.10.2021.
//

#include <stdio.h>
int main(){
    FILE *write_ptr;

    write_ptr = fopen("test.bin","wb");  // w for write, b for binary
    char *buffer = "akif kaartla";
    fwrite(buffer,sizeof(buffer),1,write_ptr); // write 10 bytes from our buffer
    return 0;
}