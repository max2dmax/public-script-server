#!/bin/bash

loading_bar() {
    local current=$1
    local total=$2
    local percent=$((current * 100 / total))
    local bar_length=55  # Adjust this for the length of the loading bar
    local filled=$((percent * bar_length / 100))
    local empty=$((bar_length - filled))
    
    printf "\r[%-${bar_length}s] %d%%" $(printf "|%.0s" $(seq 1 $filled)) $percent
}

echo "   "
echo "=============================="
echo "This script will search for common macOS Panic keywords to help narrow down shutdown issues. It will 'weed out' any non-panic errors so that it's easier to pinpoint related crashes. It will also check macOS logs for application-related panic events for a more complete look at all the computer's potential shutdown causes." 
echo "   "
echo "How many hours back would you like to search the system logs for kernel panics?"
read -p "Enter the number of hours: " HOURS

OUTPUT_FILE="$HOME/Desktop/Panic_Results.txt"

echo "   "
echo "Great! Let's search the logs for the last $HOURS hour(s). This process takes a while, so just let it run in the background."
echo "A file called Panic_Results.txt will be saved to the Desktop once it's done so you can see the results. Happy troubleshooting!"
echo "   "

echo "Analyzing system logs for kernel panics and application-related panics from the last $HOURS hour(s)..." > "$OUTPUT_FILE"

PANIC_KEYWORDS=(
    "panic\(cpu"
    "Machine Check Exception"
    "No HPETs available"
    "Kernel Extension in Backtrace"
    "Debugger message: panic"
    "BSD process name corresponding to current thread"
    "Unaligned trap"
    "Timeout while waiting for I/O completion"
    "Virtual memory exhausted"
    "TLB invalidation IPI timeout"
    "Sleep Wake Failure in EFI"
    "page fault"
    "memory corruption"
    "bad trap"
    "Attempt to free a block not in use"
)

PANIC_DESCRIPTIONS=(
    "General CPU-related panics. These can indicate hardware or software issues involving the CPU."
    "Hardware-related CPU issue. Often caused by failing or overheating CPU or memory."
    "CPU configuration issue. High Precision Event Timer is unavailable or misconfigured."
    "Kernel extensions (kexts) involved in the panic. Could be a third-party driver causing the issue."
    "Triggered by a software debugger. Often related to development or testing environments."
    "Identifying the application that caused the panic."
    "Memory or instruction error caused by accessing memory at an incorrect address."
    "I/O device failures. Could be related to storage devices like hard drives or SSDs."
    "The system ran out of virtual memory. Often caused by memory leaks or heavy resource usage."
    "Translation Lookaside Buffer (TLB) error related to memory address translation."
    "Sleep or wake issues often related to hardware power management."
    "Page fault error. Occurs when the system tries to access unavailable memory."
    "Detected memory corruption, often caused by faulty RAM or a software bug."
    "Illegal memory or instruction access, often indicative of deeper system issues."
    "Memory management bug where an attempt is made to free unallocated memory."
)

total_keywords=${#PANIC_KEYWORDS[@]}

# Loop through keywords and analyze logs
for i in "${!PANIC_KEYWORDS[@]}"; do
    keyword="${PANIC_KEYWORDS[$i]}"
    description="${PANIC_DESCRIPTIONS[$i]}"
    echo " "
    echo "Checking for panics related to '$keyword'..."
    echo "==============================" >> "$OUTPUT_FILE"
    echo "Kernel Panics Matching '$keyword' (Last $HOURS Hour(s)):" >> "$OUTPUT_FILE"
    echo "Description: $description" >> "$OUTPUT_FILE"
    echo "==============================" >> "$OUTPUT_FILE"
    
    # Perform the actual log check and append results to the output file
    log show --predicate "eventMessage contains '$keyword'" --last "${HOURS}h" >> "$OUTPUT_FILE"
    echo -e "\n" >> "$OUTPUT_FILE"
    
    loading_bar $((i + 1)) $total_keywords
done

echo " "
echo "Checking for application-related panics..."
echo "=========================================="
echo "Processing collected data..."
echo "==============================" >> "$OUTPUT_FILE"
echo "Application-Caused Kernel Panics (Last $HOURS Hour(s)):" >> "$OUTPUT_FILE"
echo "Description: Panics caused by applications, indicated by the BSD process name." >> "$OUTPUT_FILE"
echo "==============================" >> "$OUTPUT_FILE"

log show --predicate 'eventMessage contains "BSD process name corresponding to current thread"' --last "${HOURS}h" >> "$OUTPUT_FILE"
echo -e "\n" >> "$OUTPUT_FILE"

echo " "
echo "Analysis complete. Check the 'Panic_Results.txt' file on your Desktop."