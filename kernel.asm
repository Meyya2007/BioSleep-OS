org 0x7c00          ; Tell the system this code runs at the standard boot sector address
bits 16             ; Set processor to 16-bit real mode

start:
    mov ax, 0x0003  ; Clear the screen and force standard 80x25 text mode
    int 0x10

    mov si, msg     ; Load our green status tracking message into memory
print_loop:
    lodsb
    cmp al, 0
    je halt_loop
    mov ah, 0x0e    ; Print character to the screen matrix
    int 0x10
    jmp print_loop

halt_loop:
    hlt             ; --- HARDWARE INTEL POWER HALT (0% CPU OVERHEAD) ---
    in al, 0x60     ; Read the raw biosensor input port
    cmp al, 0x1E    ; Check if the 'A' key (simulated mutation event) is pressed
    jne halt_loop

    mov si, alert   ; Load our red alert warning message into memory
alert_loop:
    lodsb
    cmp al, 0
    je halt_loop
    mov ah, 0x0e    ; Print the red mutation alert text to screen
    int 0x10
    jmp alert_loop

msg db 13, 10, "BioSleep OS: Active. Monitoring Microbe/Plant DNA Sensors...", 0
alert db 13, 10, "[ALERT] CRITICAL GENETIC MUTATION DETECTED!", 0

times 510-($-$$) db 0   ; Pad the file with zeros up to exactly 510 bytes
dw 0xAA55               ; Add the mandatory 2-byte magic boot token signature
