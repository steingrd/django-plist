#include <stdio.h>
#import <Foundation/foundation.h>

int main(int argc, const char* argv[])
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    
    NSDictionary *dictionary = [NSDictionary dictionaryWithContentsOfFile:@"test_dict.plist"];
    
    NSUInteger expected = 7;
    
    if ([dictionary count] == expected) {
        printf("OK\n");
    } else {
        printf("FAILED %d != %d\n", (unsigned int)[dictionary count], (unsigned int)expected);
    }
    
    [pool release];
    return 0;
}