###########################################
# Script to generate a HTML report from a 
# SQLMap stdout output
#
# Author : Dominique Righetto 
#          dominique.righetto@owasp.org
# Date   : March 2012
###########################################
import sys
#I/O paths, take SQLMap STDOUT file from script parameter
stdout_file_path = sys.argv[1]
report_file_path = stdout_file_path + ".html"
#Open STDOUT file in read mode
file_handle_read = open(stdout_file_path,"r")
#Open REPORT file in write mode
file_handle_write = open(report_file_path,"w")
#Initialize HTML report stream
file_handle_write.write("<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">")
file_handle_write.write("<head><link rel=\"StyleSheet\" href=\"style.css\" type=\"text/css\" media=\"screen\" /><title>SQLMap HTML Report</title></head>")
file_handle_write.write("<body><table id=\"myStyle\">")
file_handle_write.write("<thead><tr><th scope=\"col\">Test datetime</th><th scope=\"col\">Test description</th></tr></thead>")
file_handle_write.write("<tbody>")
#Flag to know is global audit is OK
cannot_find_injectable_parameter = False
#Read STDOUT file line by line
for line in file_handle_read:
    if (line.strip().startswith("[")) and (line.find("[*]") == -1):
        #Check for special message indicating audit global status
        if(line.lower().find("all parameters are not injectable") > -1):
            cannot_find_injectable_parameter = True
        #Report generation
        line_part = line.strip().split(" ") 
        if (line_part[2].lower() == "testing"):
            #Extract useful informations
            execution_datatime = line_part[0]
            execution_trace = ""
            count = 2
            while(count < len(line_part)):
                execution_trace = execution_trace + " " + line_part[count]
                count = count + 1 
            #Write report HTML line
            file_handle_write.write("<tr><td>" + line_part[0] + "</td><td>" + execution_trace + "</td></tr>")                
file_handle_write.write("</tbody></table>")        
#Write global audit stauts line
if(cannot_find_injectable_parameter):
    file_handle_write.write("<h1 class=\"success\">SQLMap has found injectable parameters !</h1>")
else:
    file_handle_write.write("<h1 class=\"fail\">SQLMap could not find injectable parameters !</h1>")
#Finalize report HTML stream
file_handle_write.write("</body></html>")
#Close I/O stream    
file_handle_write.close()
file_handle_read.close()
#Print some informations
print "Report generated to " + report_file_path 
