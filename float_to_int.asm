section .text
global float_to_int_asm

; Input:
;   xmm0: Single-precision floating-point value
; Output:
;   eax: Integer value

float_to_int_asm:
    push rbp
    mov rbp, rsp
    movss xmm0, [rbp + 16]
    cvttss2si eax, xmm0       ; Convert single-precision float to integer
    add eax, 1
    leave
    ret                        ; Return
