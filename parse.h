#include <stdio.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <stdlib.h>
#include <string.h>

#define parameter_array_size 100
#define parameter_strings_long 100
#define variable_array_size 30

struct parameter_list
{
    _Bool must;
    int count;
    char parameter[variable_array_size][parameter_strings_long];
};

char file_parameter[parameter_strings_long];
struct parameter_list parameter[parameter_array_size];
int parameter_count;

void parse_xml(char *xml_posion);
