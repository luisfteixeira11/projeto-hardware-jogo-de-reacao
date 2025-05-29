import random
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) ##seta o sensor
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
top_tempos = [0, 0, 0, 0, 0]
top_nomes = ["", "", "", "", ""] ##para o sistema de pontuação
lugar = -1
contavitorias = 0
 
verde = False
amarelo = False
vermelho = False
fimdoprograma = False
atualizado = False
errado = False
 
GPIO.setup(17, GPIO.OUT)  # vermelho
GPIO.setup(22, GPIO.OUT)  # verde
GPIO.setup(27, GPIO.OUT)  # amarelo
 
def iniciar():
    global fimdoprograma
    x = input("Escreva 'vamos' abaixo pra iniciar quando tu tiver pronto, se quiser terminar digite 'xao' :)\n")
 
    while x.lower() != 'vamos' and x.lower() != 'xao':
        x = input("Deixe de resenha vá\n")
        print("")
    if x.lower() == 'xao':
        fimdoprograma = True
 
def luzes_acendem(): ##todas as luzes vao acendendo como um sinal de transito no intervalo de 0.5s e depois apagam
    GPIO.output(17, GPIO.HIGH)  # vermelho
    time.sleep(1)
    GPIO.output(27, GPIO.HIGH)  # amarelo
    time.sleep(1)
    GPIO.output(22, GPIO.HIGH)  # verde
    time.sleep(1)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
   
def luzes_comemoram():
    for _ in range(5):  # piscam 5 vezes se entrar no ranking
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(27, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        time.sleep(0.2)
       
def luzes_tristes():
    # pisca o vermelho 3 vezes para tristeza
    for _ in range(3):
        GPIO.output(17, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(17, GPIO.LOW)
        time.sleep(0.3)
       
def luzes_recorde():
    for _ in range(7):
        GPIO.output(22, GPIO.HIGH)  ##verde varias vezes
        time.sleep(0.15)
        GPIO.output(22, GPIO.LOW)
        time.sleep(0.15)
       
def luzes_aplaudem():
    for _ in range(7):
        GPIO.output(17, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(22, GPIO.LOW)
       
def luzes_rodadaesp():
    for _ in range(6):
        GPIO.output(17, GPIO.HIGH)  # vermelho
        time.sleep(0.2)
        GPIO.output(27, GPIO.HIGH)  # amarelo
        time.sleep(0.2)
        GPIO.output(22, GPIO.HIGH)  # verde
        time.sleep(0.2)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
 
def medir_distancia(): ##calcula a distância medida pelo sensor ultrassonico
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.000002)
 
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()
 
    pulse_duration = pulse_end - pulse_start
    distancia = pulse_duration * 17150 ##agora tá em milissegundos
    return round(distancia, 2)
 
def cronometro_de_espera(tempolim): ##da um tempo de espera para concentração
    global errado
    agora = time.time()
    while True:
        tempo_atual = time.time()
        tempo_decorrido = tempo_atual - agora
        distancia = medir_distancia()
        if distancia <= 60:
            luzes_tristes()
            time.sleep(1)
            print("KKKKKKKK queimou a largadapae")
            print("")
            errado = True
            return False
        elif tempolim <= tempo_decorrido:
            largada(random.randint(1,3))
            return True
        time.sleep(0.001)
 
def largada(x): ##acende uma luz, assim, dando o necessário para o jogador acionar o sensor na distância pedida
    global verde, amarelo, vermelho
    verde = False
    amarelo = False
    vermelho = False
 
    if x == 1:
        GPIO.output(22, GPIO.HIGH)  # verde
        verde = True
    elif x == 2:
        GPIO.output(17, GPIO.HIGH)  # vermelho
        vermelho = True
    else:
        GPIO.output(27, GPIO.HIGH)  # amarelo
        amarelo = True
 
def cronometro_reacao():
    global lugar, contavitorias, errado
    agora = time.time()
 
    while True:
        dist = medir_distancia()
        tempo_decorrido = time.time() - agora
        if dist <= 60:
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            # acertou a cor e a distância
            if verde and dist <= 20:
                tempo_e_dist(tempo_decorrido, dist)
                lugar = atualizar_top5(tempo_decorrido)
                contavitorias+=1
                return lugar
            elif amarelo and 20 < dist <= 40:
                tempo_e_dist(tempo_decorrido, dist)
                lugar = atualizar_top5(tempo_decorrido)
                contavitorias+=1
                return lugar
            elif vermelho and 40 < dist <= 60:
                tempo_e_dist(tempo_decorrido, dist)
                lugar = atualizar_top5(tempo_decorrido)
                contavitorias+=1
                return lugar
            # errou a cor ou a distância
            else:
                print("Tuderrado")
                print("")
                luzes_tristes()
                time.sleep(1)
                tempo_e_dist(tempo_decorrido, dist)
                errado = True
                return -1
        if tempo_decorrido > 10:
            print("esquecesse foi?kkkkkkkkkkkkkkkkkkkkk")
            print("")
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            return -1
        time.sleep(0.001)
 
def tempo_e_dist(tempo_decorrido, dist): ##printa no terminal o tempo e a distancia
    global verde, amarelo, vermelho
    tempo = tempo_decorrido*1000
    print(f"Tempo de Reação: {tempo:.2f} milissegundos")
    print("")
    print(f"Verde: {verde}, Amarelo: {amarelo}, Vermelho: {vermelho}, Distância: {dist}")
    print("")
    print(f"Distância: {dist:.2f} cm")
    print("")
   
def atualizar_top5(tempo):
    global top_tempos, top_nomes, atualizado
    tempo *=1000
    # se for o pior, não entra no ranking
    if tempo > top_tempos[4] and top_tempos[4] != 0:
        return -1
 
    pos = 4
    while pos > 0 and (top_tempos[pos - 1] == 0 or tempo < top_tempos[pos - 1]):
        top_tempos[pos] = top_tempos[pos - 1]
        top_nomes[pos] = top_nomes[pos - 1]
        pos -= 1
 
    top_tempos[pos] = tempo
    top_nomes[pos] = ""  # preenchido depois
    atualizado = True
    return pos
 
def cronometroesp1(vd, am ,vm): ##nao acerte os que acenderam
    global contavitorias
    agora = time.time()
    while True:
        dist = medir_distancia()
        tempo_decorrido = time.time() - agora
        if dist <= 60:
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            # acertou a cor e a distância
            if vd==False and dist <= 20:
                print("ok...")
                luzes_aplaudem()
                tempo_e_dist(tempo_decorrido, dist)
                contavitorias+=1
                return lugar
            elif am==False and 20 < dist <= 40:
                print("ok...")
                luzes_aplaudem()
                tempo_e_dist(tempo_decorrido, dist)
                contavitorias+=1
                return lugar
            elif vm==False and 40 < dist <= 60:
                print("ok...")
                luzes_aplaudem()
                tempo_e_dist(tempo_decorrido, dist)
                contavitorias+=1
                return lugar
            else:
                print("ai nao pokk")
                print("")
                luzes_tristes()
                return 0
       
        if tempo_decorrido > 10:
            print("pobicho?kkkkkkkkkkkkkkkkkkkkk")
            print("")
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            return -1
        time.sleep(0.001)
       
def cronometroesp2(): ##nao toque em nenhum
    global contavitorias
    agora = time.time()
    while True:
        dist = medir_distancia()
        tempo_decorrido = time.time() - agora
        if dist <= 60:
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            print("ainaovei")
            luzes_tristes()
            return 0
       
        if tempo_decorrido > 10:
            print("boa bicho, atento")
            print("")
            luzes_aplaudem()
            contavitorias+=1
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            return -1
        time.sleep(0.001)
   
def cronometroesp3(vd, am, vm): ##toque em algum que esteja apagado
    global contavitorias
    agora = time.time()
    while True:
        dist = medir_distancia()
        tempo_decorrido = time.time() - agora
        if dist <= 60:
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            # acertou a cor e a distância
            if vd==False and dist <= 20:
                print("Certo...")
                luzes_aplaudem()
                tempo_e_dist(tempo_decorrido, dist)
                contavitorias+=1
                return lugar
            elif am==False and 20 < dist <= 40:
                print("Certo...")
                luzes_aplaudem()
                tempo_e_dist(tempo_decorrido, dist)
                contavitorias+=1
                return lugar
            elif vm==False and 40 < dist <= 60:
                print("Certo...")
                luzes_aplaudem()
                tempo_e_dist(tempo_decorrido, dist)
                contavitorias+=1
                return lugar
            else:
                print("ai nao pokk")
                print("")
                time.sleep(1.5)
                luzes_tristes()
                return 0
       
        if tempo_decorrido > 10:
            print("pobicho?kkkkkkkkkkkkkkkkkkkkk")
            print("")
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            return -1
        time.sleep(0.001)
 
 
def rodada_surpresa ():
    print("Rodada Surpresa... Pra te atrapalhar >:)")
    luzes_rodadaesp()
    xesp = random.randint(1, 3)
    if(xesp == 1):
        print("Acerte o led que nao acendeu")
        xs = random.randint(1, 3)
        xs2 = random.randint(1, 3)
        vd, vm, am = False, False, False
        while(xs2 == xs):
            xs2 = random.randint(1, 3)
        if xs == 1 or xs2 == 1:
            GPIO.output(22, GPIO.HIGH)  # verde
            vd = True
        elif xs == 2 or xs2 == 2:
            GPIO.output(17, GPIO.HIGH)  # vermelho
            vm = True
        elif xs==3 or xs2 == 3:
            GPIO.output(27, GPIO.HIGH)  # amarelo
            am = True
        cronometroesp1(vd, am, vm)
        time.sleep(1)
       
    elif (xesp == 2):
        print ("Não acione nenhum led")
        time.sleep(2)
        xs = random.randint(1, 3)
        if xs == 1:
            GPIO.output(22, GPIO.HIGH)  # verde
        elif xs == 2:
            GPIO.output(17, GPIO.HIGH)  # vermelho
        else:
            GPIO.output(27, GPIO.HIGH)  # amarelo
        cronometroesp2()
        time.sleep(1)
       
    else:
        print("Não acerte o led que acendeu")
        time.sleep(2)
        xs = random.randint(1, 3)
        vd, vm, am = False, False, False
        if xs == 1:
            GPIO.output(22, GPIO.HIGH)  # verde
            vd = True
        elif xs == 2:
            GPIO.output(17, GPIO.HIGH)  # vermelho
            vm = True
        else:
            GPIO.output(27, GPIO.HIGH)  # amarelo
            am = True
        cronometroesp3(vd, am, vm)
        time.sleep(1)
    time.sleep(0.5)
    print("")
    print("Fim da Rodada Especial!")
    print("")
    time.sleep(0.2)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    luzes_rodadaesp()
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
       
           
   
 
 
while not fimdoprograma:
    iniciar()
    if fimdoprograma:
        print("Jogo encerrado.")
        break
    print("Para terminar no meio do jogo basta apertar Ctrl + C")
    print("")
    while True:
        try:
            errado = False
            luzes_acendem()
            if (contavitorias%5==0 and contavitorias>=5):
                time.sleep(1)
                print("Calma, calma...")
                rodada_surpresa()
                continue
            if cronometro_de_espera(random.randint(2, 10)):
                lugar = cronometro_reacao()
                time.sleep(2)
            else:
                tempo_e_dist(0, medir_distancia())
                time.sleep(2)
            if atualizado and lugar != -1:
                nomao = input("Bota teu nome que tu ganhou: ").strip()
                luzes_comemoram()
                if not nomao:
                    nomao = "nao botou nada pq quis"
                print("")
                if lugar == 0:
                    luzes_recorde()
                top_nomes[lugar] = nomao
                print("\nRanking Top 5 Tempos de Reação:")
                for i in range(5):
                    if top_tempos[i] != 0:
                        print(f"{i+1}º: {top_nomes[i]} - {top_tempos[i]:.2f} milissegundos")
                    print("")
                atualizado = False
            if contavitorias >= 3:
                luzes_aplaudem()
                print("Você atingiu 3 ou mais vitórias")
                print("")
            print(f"Seu número de vitórias é: {contavitorias}")
            if errado:
                fimdoprograma = True
                try:
                    p = int(input("Quer continuar?? digite 1\n"))
                except ValueError:
                    p = 0
                if p == 1:
                    fimdoprograma = True
                    continue
                break
        except KeyboardInterrupt:
            amarelo = False
            vermelho = False
            verde = False
            GPIO.cleanup()
            fimdoprograma = True
            break

        vermelho = False
        amarelo = False
        verde = False
    if fimdoprograma:
        print("Jogo encerrado.")
        print("\nRanking Top 5 Tempos de Reação:")
        for i in range(5):
            if top_tempos[i] != 0:
                print(f"{i+1}º: {top_nomes[i]} - {top_tempos[i]:.2f} milissegundos")
            print("")
        try:
            jogardnv = int(input("Digite '1' para jogar novamente...\n"))
        except ValueError:
            jogardnv = 0
        if jogardnv == 1:
            fimdoprograma = False
            continue
        GPIO.cleanup()
        break
 
