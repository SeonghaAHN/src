/*

마이크로컨트롤러 과제
Author : SeongHa Ahn
Github : https://github.com/SeonghaAHN

*/

#include <mega128a.h>
#include <delay.h>
#include <stdbool.h>

typedef unsigned char u_char;
typedef unsigned int u_int;

const u_char seg[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 
                        0x6D, 0x7D, 0x07, 0x7F, 0x6F};  //세그먼트

const u_char asc[12] = {0x30, 0x31, 0x32, 0x33, 0x34, 
                        0x35, 0x36, 0x37, 0x38, 0x39, 
                        0x2E, 0x20};                    //아스키코드

u_char flag_ext_int4, flag_ext_int5, flag_ext_int6, flag_ext_int7 = 0;    //ISR 수행 위한 flag
u_char led = 0b11111100;                                //LED 초기값
u_char flag_timer1, flag_timer0 = 0;                    //타이머 사용을 위한 flag
u_char cnt_for_timer0, cnt_for_int7 = 0;                //인터럽트 카운트 위한 flag
u_int tcnt_for_timer1 = 0x551A;                         //타이머 1 초기값 : 21786, 1 cycle == (0.064msec*43750 ==2800msec)
u_int ocr_for_timer0 = 124;                             //출력비교 레지스터 값 설정, 1 cycle == (16000usec*125 == 8msec)
u_int num1 = 2015;                                      //학번 앞자리
u_int num2 = 2259;                                      //학번 뒷자리
u_int  k, i, adc = 0;                                   //변수 설정
u_int ival;                                             //변수 설정
float val, fval;                                        //변수 설정

void initial_setting();                                 //포트 입출력 초기설정
void seg_display(int num1, bool decimal_point);         //세그먼트 표시
void ext_int4();                                        //EXT INT4 ISR                     
void usart_setting();                                   //usart 사용을 위한 레지스터 세팅
void int5_timer0_start();                               //int5 발생 시 사용할 타이머0 설정
void timer0();                                          //타이머0 를 이욯안 800msec 대기 후 수행할 프로그램
void int6_timer1_start();                               //int6 발생 시 사용할 타이머1 설정
void timer1();                                          //타이머1 를 이용한 2800msec 대기 후 수행할 프로그램
void int_disable();                                     //int7 제외한 인터럽트 disable
void int_enable();                                      //전 인터럽트 enable
void clear_all_flag();                                  //ISR 수행 중 발생한 flag clear

void main(void){                                        //main문
    
    initial_setting();                                  //초기설정

    for (i = 0; i < 100; i++){                          //(1 cycle of seg_display func)0.02sec*100 = 2sec
        seg_display(num1, false);                       // 학번 앞자리 2초간 표시
    }

    while(1){
        for (i = 0; i < 50; i++){                       //1 cycle == (0.02sec * 50 == 1 sec) + a
            seg_display(num2, false);                   //학번 뒷자리 세그먼트 표시
            if (flag_ext_int4 == 1){                    //EXT INT4 서비스루틴 실행을 위한 flag 확인
                ext_int4();                             //LED 2개 ON, Shift
            }
            if (flag_ext_int5 == 1){                    //EXT INT5 서비스루틴 실행을 위한 flag 확인
                int5_timer0_start();                    //timer0 사용을 위한 세팅
                while(cnt_for_timer0 != 100);           //8msec * 100== 800msec 대기
                timer0();                               //ADC 전압 측정 후 USART 송신
            }
            if(flag_ext_int6 == 1){                     //EXT INT6 서비스루틴 실행을 위한 flag 확인
                int6_timer1_start();                    //timer1 사용을 위한 세팅
                while(flag_timer1 == 0);                //2800msec 대기
                timer1();                               //온도 측정, 세그먼트 표시
            }
            if(flag_ext_int7 == 1){                     //EXT INT7 서비스루틴 실행을 위한 flag 확인
                int_disable();                          //INT7을 제외한 인터럽트 disable
                while(cnt_for_int7 != 7);               //INT7이 7번 발생할 때까지 대기
                int_enable();                           //INT 4,5,6,7 enable
            }       
        }

        for (i = 0; i < 200; i++){                      //1 cycle == (0.005 sec * 200 == 1 sec) + a
            PORTG = 0x00;                               //seg off
            delay_ms(5);                                //주기 설정을 위해 0.005 sec delay
            if (flag_ext_int4 == 1){                    //EXT INT4 서비스루틴 실행을 위한 flag 확인
                ext_int4();                             //LED 2개 ON, Shift
            }
            if (flag_ext_int5 == 1){                    //EXT INT5 서비스루틴 실행을 위한 flag 확인
                int5_timer0_start();                    //timer0 사용을 위한 세팅
                while(cnt_for_timer0 != 100);           //8msec * 100== 800msec 대기
                timer0();                               //ADC 전압 측정 후 USART 송신
            }
            if(flag_ext_int6 == 1){                     //EXT INT6 서비스루틴 실행을 위한 flag 확인
                int6_timer1_start();                    //timer1 사용을 위한 세팅
                while(flag_timer1 == 0);                //2800msec 대기
                timer1();                               //온도 측정, 세그먼트 표시
            }
            if(flag_ext_int7 == 1){                     //EXT INT7 서비스루틴 실행을 위한 flag 확인
                int_disable();                          //INT7을 제외한 인터럽트 disable
                while(cnt_for_int7 != 7);               //INT7이 7번 발생할 때까지 대기
                int_enable();                           //INT 4,5,6,7 enable
            } 
        }
    }
}          

interrupt [EXT_INT4] void external_int4(void){          //EXT INT4
    SREG &= 0x7F;                                       //All interrupt disable
    flag_ext_int4 = 1;                                  //while문에서 ISR 처리 위한 flag 변경
    SREG |= 0X80;                                       //All interrupt enable
}

interrupt [EXT_INT5] void external_int5(void){          //EXT INT5
    SREG &= 0x7F;                                       //All interrupt disable
    flag_ext_int5 = 1;                                  //while문에서 ISR 처리 위한 flag 변경
    SREG |= 0X80;                                       //All interrupt enable
}

interrupt [EXT_INT6] void external_int6(void){          //EXT INT6
    SREG &= 0x7F;                                       //All interrupt disable
    flag_ext_int6 = 1;                                  //while문에서 ISR 처리 위한 flag 변경
    SREG |= 0X80;                                       //All interrupt enable
}

interrupt [EXT_INT7] void external_int7(void){          //EXT INT7
    SREG &= 0x7F;                                       //All interrupt disable
    flag_ext_int7 = 1;                                  //while문에서 ISR 처리 위한 flag 변경
    cnt_for_int7++;                                     //인터럽트 발생 시 cnt 1씩 증가
    SREG |= 0X80;                                       //All interrupt enable
}

interrupt [TIM0_COMP] void timer0_comp(void){           //Timer0 compare
    SREG &= 0x7F;                                       //All interrupt disable
    cnt_for_timer0++;                                   //인터럽트 발생 시 cnt 1씩 증가
    SREG |= 0X80;                                       //All interrupt enable
}

interrupt [TIM1_OVF] void timer1_ovf(void){             //Timer1 overflow
    SREG &= 0x7F;                                       //All interrupt disable
    flag_timer1 = 1;                                    //while문에서 ISR 처리 위한 flag 변경
    SREG |= 0X80;                                       //All interrupt enable    
}

void initial_setting(void){                             //초기 설정
    DDRC = 0XFF;                                        //PORTC OUTPUT    
    DDRE = 0x00;                                        //PORTE 4,5,6,7 입력
    DDRB = 0xf0;                                        //세그먼트 출력 설정
    DDRD = 0XF0;                                        //세그먼트 출력 설정
    DDRG = 0X0F;                                        //세그먼트 출력 설정
    PORTC = 0xFF;                                       //LED off
    SREG = 0X80;                                        //인터럽트 enable
    EIMSK = 0b11110000;                                 //EXT INT 4567 enable
    EICRB = 0b11111010;                                 //INT4 Falling / INT5 Falling / INT6 Rising / INT7 Rising
}
     
void seg_display(int num1,  bool decimal_point){        //세그먼트 표시 num1 : 표시할 숫자 decimal_point : 소수점 (첫째자리) 표시
    int n1000, n100, n10, n1, buf;                      //변수설정
    int a = 1, num2 = 0;                                //num2 : 세그먼트에 표시할 자릿수
    while( num1 > a ){                                  //표시할 자릿수 구하기
        a *= 10;                                        
        num2++;
    }                                                   
    n1000 = num1/1000;                                  //1000자리수
    buf = num1%1000;                        
    n100 = buf/100;                                     //100자리수
    buf = buf%100;
    n10 = buf/10;                                       //10자리수
    n1 = buf%10;                                        //1자리수

    if(num2>0){
        PORTG = 0b00001000;                             //세그먼트 1자리
        PORTD = ((seg[n1] & 0x0F)<<4)|(PORTD&0x0F);     //세그먼트 1자리 4개 on           
        PORTB = ((seg[n1] & 0x70)|(PORTB & 0x0F));      //세그먼트 1자리 4개 on 
        delay_ms(5);
    }
        
    if(num2>1){
        PORTG = 0b00000100;                             //세그먼트 10자리수
        PORTD = ((seg[n10] & 0x0F)<<4)|(PORTD&0x0F);    //반복            
        PORTB = (seg[n10] & 0x70)|(PORTB & 0x0F);
        if(decimal_point == true) PORTB = PORTB|0x80;   //소수점 표시 
        delay_ms(5);
    }

    if(num2>2){
        PORTG = 0b00000010;                             //세그먼트 100자리수
        PORTD = ((seg[n100] & 0x0F)<<4)|(PORTD&0x0F);            
        PORTB = (seg[n100] & 0x70)|(PORTB & 0x0F);
        delay_ms(5);
    }
    
    if(num2>3){
        PORTG = 0b00000001;                             //세그먼트 1000자리수
        PORTD = ((seg[n1000] & 0x0F)<<4)|(PORTD&0x0F);            
        PORTB = (seg[n1000] & 0x70)|(PORTB & 0x0F);
        delay_ms(5);
    }

    PORTG = 0X0;                                        //세그먼트 off
}

void ext_int4(void){                                    //EXT INT4 발생 시 실행 : LED 2개 ON, Shift
    PORTC = led;                                        //LED on
    led = led << 2;                                     //LED shift
    led = led | 0b00000011;                             //off the last 2 LED
    if (PORTC == 0xFF) led = 0XFC;                      //initialize
    clear_all_flag();                                   //프로그램 수행 중 발생한 인터럽트 flag clear
}

void usart_setting(){                                   //USART 통신 위한 setting
    UCSR0A = 0x0;                                       //USART 초기화
    UCSR0B = 0x08;                                      //송신 enable 
    UCSR0C = 0x06;                                      //비동기, 데이터 8비트 모드
    UBRR0H = 0;                                         //BAUD == 9600
    UBRR0L = 103;
}

void int5_timer0_start(void){                           //EXT INT5 발생 시 실행 : timer0 사용 위한 세팅
    TIMSK = 0x02;                                       //timer interrupt enable
    TCCR0 = 0x0F;                                       //CTC mode / 1024분주
    OCR0 = ocr_for_timer0;                              //출력비교 레지스터 값 설정, 1 cycle == (16000usec*125 == 8msec)
    TCNT0 = 0;                                          //초기값 = 0
}

void timer0(void){
    u_int m = 1;                                        //변수설정

    usart_setting();                                    //USART 통신 위한 setting
    
    ADMUX = 0x06;                                       //ADC 단극성 입력 선택(전압)
    ADCSRA = 0x87;                                      //16메가헤르츠 256분주 125키로헤르츠 일반 모드 
    ADCSRA = 0xC7;                                      //변환시작
   
    while((ADCSRA&0x10)==0);                            //레지스터 1될때까지 대기
    val = (int)ADCL + ((int)ADCH<<8);                   //AD변환값 읽기
    fval = (float)val*5.0/1024.0;                       //전압값으로 변환
    for(k=0;k<4;k++){                                   //USART로 송신
        adc = ((int)(fval*m))%10;                       //변환된 값 정수형 변환
        if(k==1){                                       //첫 숫자후 소수점 표시
            while((UCSR0A & 0x20)==0x0);                //송신준비까지 대기
            UDR0 = asc[10];                             //소수점 표시
        }
        while((UCSR0A & 0x20)==0x0);                    //송신준비까지 대기
        UDR0 = asc[adc];                                //숫자 표시
        m*=10;
    }
    while((UCSR0A & 0x20)==0x0);                        //송신준비까지 대기
    UDR0 = asc[11];                                     //이전 수신값과 구분하기 위한 스페이스
    
    TIMSK = 0x00;                                       //타이머 초기화
    flag_timer0 = 0;                                    //타이머 인터럽트 서비스루틴 종료
    cnt_for_timer0 = 0;                                 //800msec 주기 확인을 위한 cnt 초기화
    clear_all_flag();                                   //프로그램 수행 중 발생한 인터럽트 flag clear
}

void int6_timer1_start(void){                           //INT6 발생 시 실행 : 타이머1 사용 위한 세팅
    TIMSK = 0x04;                                       //timer interrupt enable
    TCCR1A = 0x00;                                      //OVF mode
    TCCR1B = 0x05;                                      //1024분주
    TCCR1C = 0x00;
    TCNT1 = tcnt_for_timer1;                            //타이머 1 초기값 : 21786 / 1 cycle == (0.064msec*43750 ==2800msec)
}

void timer1(void){                                      //타이머1 ovf 발생시
    ADMUX = 0x07;                                       //ADC 단극성 입력 선택(온도)
    ADCSRA = 0xE7;                                      //256분주
    delay_ms(5);   

    val = (int)ADCL + ((int)ADCH << 8);                 //AD변환값 읽기 
    fval = (float)val*5.0 / 1023.0;                     //온도로 변환
    ival = (int)(fval*1000.0+0.5);                      //정수형으로 정리
    
    for (i = 0; i < 50; i++){                           //1초간 세그먼트에 온도 표시
        seg_display(ival, true);    
    }
    
    flag_timer1 = 0;                                    //타이머 인터럽트 서비스루틴 종료
    TIMSK = 0x00;                                       //타이머 초기화
    clear_all_flag();                                   //프로그램 수행 중 발생한 인터럽트 flag clear
}

void int_disable(void){
    EIMSK = 0b10000000;                                 //EXT INT7 제외하고 disable
    EICRB = 0b11000000;                                 //EXT INT7 Rising edge
}

void int_enable(void){
    EIMSK = 0b11110000;                                 //EXT INT 4567 enable
    EICRB = 0b11111010;                                 //INT4 Falling / INT5 Falling / INT6 Rising / INT7 Rising
    cnt_for_int7 = 0;                                   //인터럽트 disable이후 발생한 cnt clear
    clear_all_flag();                                   //프로그램 수행 중 발생한 인터럽트 flag clear
}

void clear_all_flag(void){
    flag_ext_int4 = 0;                                  //ISR 수행중 발생한 flag clear
    flag_ext_int5 = 0;                                  //ISR 수행중 발생한 flag clear
    flag_ext_int6 = 0;                                  //ISR 수행중 발생한 flag clear
    flag_ext_int7 = 0;                                  //ISR 수행중 발생한 flag clear
}
