__asm__(".code16\n"
        ".global main\n"
        "main:\n"
        "   mov $0x0003, %ax\n" // Force set 80x25 text screen mode
        "   int $0x10\n"
        "   mov $0x07, %ah\n"   // Text attribute colors
        "   mov $msg, %si\n"
        "print_loop:\n"
        "   lodsb\n"
        "   cmp $0, %al\n"
        "   je halt_loop\n"
        "   mov $0x0e, %ah\n"
        "   int $0x10\n"
        "   jmp print_loop\n"
        "halt_loop:\n"
        "   hlt\n"             // Smart Power Halt
        "   inb $0x60, %al\n"   // Read biosensor register input
        "   cmp $0x1E, %al\n"   // Detect mutation alert trigger ('A' key)
        "   jne halt_loop\n"
        "   mov $alert, %si\n"
        "alert_loop:\n"
        "   lodsb\n"
        "   cmp $0, %al\n"
        "   je halt_loop\n"
        "   mov $0x0e, %ah\n"
        "   int $0x10\n"
        "   jmp alert_loop\n"
        "msg: .string \"\r\nBioSleep OS: Active. Monitoring Microbe/Plant DNA Sensors...\"\n"
        "alert: .string \"\r\n[ALERT] CRITICAL GENETIC MUTATION DETECTED!\"\n"
        ".fill 510-(.-main), 1, 0\n"
        ".word 0xAA55\n"); // Mandatory structural signature token

