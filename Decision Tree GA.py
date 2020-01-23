"""
@author: brahmasurya27
"""

import random 
from random import randint 
import csv 


def baca(): #membaca file .csv yaitu data_latih_opsi_2.csv
    tampung = []
    file = open('data_latih_opsi_2.csv', 'r') #membuka file .csv dengan nama data_latih_opsi_2.csv
    reader = csv.reader(file)
    for data in reader:
        tampung.append(data) #data csv disimpan di dalam array tampung
    return tampung

def baca_uji(): #membaca file .csv yaitu data_uji_opsi_2.csv
    tamp = []
    file = open('data_uji_opsi_2.csv', 'r') #membuka file .csv dengan nama data_uji_opsi_2.csv
    reader = csv.reader(file)
    for data in reader:
        tamp.append(data) #data csv disimpan di dalam array tamp
    return tamp

def individu(): #membuat kromosom yang terdiri dari 5 karakteristik yaitu:suhu (0-2), waktu(0-3), kondisi (0,3), kelembapan (0,2), aksi (0,1)
    krom = []
    length = randint(1,4) #mendefinisikan panjang rule setiap kromosom yang berbeda-beda
    for i in range(length):
        suhu = randint(0,2)
        waktu = randint(0,3)
        kondisi = randint(0,3)
        kelembapan = randint(0,2)
        aksi = randint(0,1)
        krom.append(str(suhu)) #nilai suhu yg didapatkan dari randint di simpan di dalam array krom dengan di ubah ke dalam string
        krom.append(str(waktu)) #nilai waktu yg didapatkan dari randint di simpan di dalam array krom dengan di ubah ke dalam string
        krom.append(str(kondisi)) #nilai kondisi yg didapatkan dari randint di simpan di dalam array krom dengan di ubah ke dalam string
        krom.append(str(kelembapan)) #nilai kelembapan yg didapatkan dari randint di simpan di dalam array krom dengan di ubah ke dalam string
        krom.append(str(aksi)) #nilai aksi yg didapatkan dari randint di simpan di dalam array krom dengan di ubah ke dalam string
    return krom
def populasi(jumlah):#membuat populasi yang terdiri dari sekumpulan kromosom
    pop = []
    for i in range(jumlah):
        tamp = individu() #memanggil fungsi individu yg ditampung di tamp
        pop.append(tamp)  #kromosom tersebut di simpan di dalam array pop
    return pop

def split(ukuran,individu): #fungsi split yang membuat tiap kromosom terbagi menjadi 5 gen tiap rule (suhu,waktu,kondisi,kelembapan,aksi)
    tes = []
    while len(individu) > ukuran:
        kiri = individu[:ukuran]
        tes.append(kiri)
        individu = individu[ukuran:]
    tes.append(individu) #hasil split disimpan didalam array tes
    return tes

def hitungfitnes(populasi): #fungsi yang digunakan untuk menghitung fitnes dalam kromosom dengan mencocokan dengan data_latih_opsi_2.csv jika data yang dicocokan sama akan bertambah satu
    listfitnes = []
    data = baca() #memanggil fungsi baca csv
    x = populasi 
    arrTmp = []
    for i in x:
        q = split(5,i) #mensplit tiap 5 gen pada kromosom dengan menggunakan fungsi split
        arrTmp.append(q)
    hit = 0
    for tiapIndividu in arrTmp:
        for tiapSplit in tiapIndividu:
            for setiapRule in data:
                if(len(setiapRule) == len(tiapSplit) and setiapRule == tiapSplit): # mencocokan data yang ada di csv(setiaprule) dengan data pada kromosom yang sudah di split
                    hit +=1 #jika nilai yang dicocokan sama, hit akan terus bertambah satu hingga data yang dicocokan sudah selesai
        listfitnes.append(hit/80) #fitnes tiap kromosom didapatkan dengan total nilai yang sama (hit)/80 (jumlah banyaknya data pada csv, sehingga didapatkan nilai fitnes)
        hit =0
    return listfitnes
   
def pemilihan_ortu(fitnes): #menggunakan metode pemilihan orang tua roulette wheel
    hasil=[]
    total = 0
    prop =0
    m = 0
    n = 0
    x = random.uniform(0,1)
    fit = fitnes 
    for i in fit:
        total += i #menjumlahkan keseluruhan fitnes ditampung pada total
    for j in fit:
        prop = (j/total) #membagi setiap fitnes yang sudah didaptkan dengan jumlah fitnes untuk mendapatkan proporsi
        hasil.append(prop)
    for i in (hasil):
        m =i+m #nilai proporsi akan selalu bertambah ketika nilai x yang di random lebih besar dari m
        if x < m:            
            break
        n = n+1 #untuk mendaptkan indeks parent
    return (n)

def crosover(parent1,parent2): #fungsi crossover, dengan empat kemungkinan yang dapat terjadi
    cek = True
    pil = []
    a = parent1
    b = parent2
    temp =0
    while(cek != False): #melakukan perulangan memilih tipot1 jika tipot[0]<tipot[1] maka perulangan akan berhenti dan mendapatkan tipot 1
        x = randint(1,len(a)-1)
        y = randint(3,len(a)-1)
        tipot1 =[x,y]
        if(tipot1[0]<tipot1[1]):
            cek = False
        else:
            cek = True
    jarak = tipot1[1]-tipot1[0] #rentan jarank dari tipot yang sudah didapatkan dikurangi, ditampung di jarak
    gap = jarak % 5 #jarak yang sudah didapakan di mod 5 
   
    #kemungkinan yang terjadi berdasarkan tipot1, yang nantinya digunakan pada tipot 2
    pil1 = [tipot1[0],tipot1[0]+jarak]
    pil2 = [tipot1[0],tipot1[0]+gap]
    pil3 = [tipot1[1]-jarak,tipot1[1]]
    pil4 = [tipot1[1]-gap,tipot1[1]]
    pil.append(pil1)
    pil.append(pil2)
    pil.append(pil3)
    pil.append(pil4)
    coba = randint(0,len(pil)-2)
    tipot2 = pil[coba]  #mendapatkan tipot 2 dengan menggunakan array pil berdasarkan indeks yang sudah didapatkan
    if(len(parent1)<=len(parent2)):
        if((len(parent1)<6)and(len(parent2)<6)):#kondisi pertama untuk two point
            tap = 0
            bts1 = tipot1[0]
            bts2 = tipot1[1]
            for i in (a):
                if (bts1<bts2):
                    tap = a[bts1]
                    a[bts1]= b[bts1]
                    b[bts1]= tap
                bts1 +=1   
            return a,b    
        else:
            if(gap>0): #jika gap memiliki nilai lebih besar dari 0 terjadi dua kemungkinan dapat terjadinya penambahan rule(increase) pada kromosom dan two point
                if(tipot1==tipot2):#tipot1 dengan tipot2 sama maka dari itu menggunakan two point
                    tap = 0
                    bts1 = tipot1[0]
                    bts2 = tipot1[1]
                    for i in (a):
                        if (bts1<bts2):
                            tap = a[bts1]
                            a[bts1]= b[bts1]
                            b[bts1]= tap
                        bts1 +=1     
                    return a,b
                else: # jika tipot1 dan tipot 2 tidak sama dan gap >0 maka dapat terjadinya increase penambahan rule pada kromosom ketika crossover
                    x =a[:tipot2[0]]
                    y =b[tipot2[0]:tipot2[1]] #anak pertama
                    z =a[tipot2[1]:]

                    j=b[:tipot2[0]]
                    k=a[tipot2[0]:tipot2[1]] #untuk anak kedua
                    l=a[tipot2[1]:tipot1[1]]
                    m=b[tipot2[1]:]
                
                    a =x+y+z #menggabungkan nilai yang sudah disimpan pada x,y,z untuk menghasilkan anaka pertam
                    b =j+k+l+m #menggabungkan nilai yang sudah disimpan pada j,k,l,m untuk menghasilkan anaka kedua
                    return a,b

            else:#jika gap kurang dari 0 maka menggunakan two point
                tap = 0
                bts1 = tipot1[0]
                bts2 = tipot2[1]
                for i in (a):
                    if (bts1<bts2):
                        tap = a[bts1]
                        a[bts1]= b[bts1]
                        b[bts1]= tap
                    bts1 +=1   
                return a,b
    else:
        # menggunakan single point
        n =0
        tap = 0
        y = 4
        for i in (b):
            if (n<y):
                tap = a[n]
                a[n]= b[n]
                b[n]= tap
            n +=1
    return a,b

def mutasi(a,b): #melakukan mutasi pada anak1 dan anak2 yang sudah dihasilkan ketika x hasil random kurang dari probabilitas 0.1
    x1=a
    x2=b
    prob = 0.1
    n = 0
    x = random.uniform(0,1)
    y = randint(0,4) 
    list = ['0','1']
    for i in (x1):
        if ( x < prob):
            if (y==n): 
                x1[n] = random.choice(list) #mengganti nilai berdasarkan indeks yang sudah didapatkan dari random
                break
        n += 1 
    n =0
    y = randint(0,4) 
    for i in (x2):
        if(x < prob):
            if (y==n):
                x2[n] = random.choice(list) #mengganti nilai berdasarkan indeks yang sudah didapatkan dari random
                break
        n +=1
    return x1,x2
   
def fitnes_terbaik(fitnes): #fungsi untuk mendapatkan fitnes terbaik pada generasi
    max,indeks = 0,0
    for i in range(len(fitnes)):
        if fitnes[i] > max:
            max = fitnes[i] #fitnes terbaik di tampung pada max
            indeks = i #indeks dengan fitnes terbaik di simpan pada indeks
    return max,indeks

def split_krom(ukuran): #fungsi untuk mensplit kromosom menjadi 5 gen tiap rule pada kromosom terbaik, yang hasil split tersebut digunakan untuk mendecode menjadi kalimat
    hasil_split = []
    split = krom_pilih
    while len(split) > ukuran:
        kiri = split[:ukuran]
        hasil_split.append(kiri)
        split = split[ukuran:]
    hasil_split.append(split)
    return hasil_split

def decode(hasil_split): #fungsi decode untuk mengubah dari integer menjadi kata pada kromosom terbaik 
    temp=hasil_split
    hasil_terjemahan=[]
    for data in (temp):
        suhu=""
        waktu=""
        kondisi=""
        kelembapan=""
        aksi=""
        if(len(data)==5):
            #ini mendefinisikan suhunya
            if(data[0]=='0'):
                suhu =' rendah '
            elif(data[0]=='1'):
                suhu=' normal '
            elif(data[0]=='2'):
                suhu = ' tinggi '
            #ini mendefinisika waktu
            if(data[1]=='0'):
                waktu=' siang '
            elif(data[1]=='1'):
                waktu=' pagi '
            elif(data[1]=='2'):
                waktu=' sore '
            elif(data[1]=='3'):
                waktu=' malam '
            #ini untuk mendefinisikan kondisi langit
            if(data[2]=='0'):
                kondisi=' berawan '
            elif(data[2]=='1'):
                kondisi=' cerah '
            elif(data[2]=='2'):
                kondisi=' hujan '
            elif(data[2]=='3'):
                kondisi=' rintik '
            #ini untuk mendefinisikan kelembapan
            if(data[3]=='0'):
                kelembapan =' rendah '
            elif(data[3]=='1'):
                kelembapan=' normal '
            elif(data[3]=='2'):
                kelembapan =' tinggi '
            #ini untuk terbang aksi (Ya/Tidak)
            if(data[4]=='0'):
                aksi =' Tidak '
            elif(data[4]=='1'):
                aksi=' Ya '
            gas =(suhu+waktu+kondisi+kelembapan+aksi) #hasil yang sudah didapatkan dari suhu,waktu,kondisi,kelembapan, dan aksi di simpan dalam gas
            hasil_terjemahan.append(gas) 
        else:
            pass
    return(hasil_terjemahan)

def banding_uji(tamp): #untuk membandingkan data uji dengan kromosom terbaik untuk mendapatkan keputusan
    tampung =[]
    tamp = tamp
    data = baca_uji()
    for split in tamp:
        for dt in data:
            if(split[0:4]==dt):
                keputusan = split[4] #jika data anatara split dengan data uji sama, nilai split indeks ke 4 di tampung di keputusan
                tampung.append([keputusan,dt]) #menampung keputusan pada array tampung 0/1 dengan nilai dari data uji
    return tampung


#---------------------------------------------------------------MAIN PROGRAM----------------------------------------------------------------#
if __name__=='__main__': #main program
    a=20 #mendeklarasikan a dengan 20
    pop = populasi(a) #memasukan nilai a pada fungsi populasi dengan minyimpan pada pop
    tampung = hitungfitnes(pop) #dari populasi dihitung fitnesnya dengan memasukan variabel pop pada fungsi hitungfitnes
    fit_global = fitnes_terbaik(tampung) #fitnes terbaik disimpan di dalam fit_global
    i=0
    fitbagus=[]
    while i <= 50: #perulangan dengan while untuk melakukan generasi sesuai jumlah perulangan yang didefinisikan
        simpan = []
        for j in range (int(a/2)):
            tampung = hitungfitnes(pop) #fitnes di tampung di variabel tampung
            idx1 = pemilihan_ortu(tampung) #idx1 digunakan untuk menyimpan indeks parent 1
            idx2 = pemilihan_ortu(tampung) #idx2 digunakan untuk menyimpan indeks parent 2
            prt1=pop[idx1] #menyimpan kromosom parent 1 di variabel prt1
            prt2=pop[idx2] #menyimpan kromosom parent 2 di variabel prt2
            anak1,anak2 = crosover(prt1,prt2) #melaukukan crossover dengan memanggil fungsi crosover dengan memasukan variabel prt1 dan prt 2 kedalam fungsi
            mts1,mts2 = mutasi(anak1,anak2) #melaukan mutasi denga memasukan variabel anak1,anak 2 ke dalam fungsi mutasi
            simpan.append(mts1) #hasil kromosom mutasi1 dan mutasi 2 disimpan di array simpan
            simpan.append(mts2)
        pop_lokal = simpan
        hasil_fitlokalisasi = hitungfitnes(pop_lokal)#menghitung fitnes dari pop_lokal
        fit_baik = fitnes_terbaik(hasil_fitlokalisasi) #membandingkan nilai fitnes terbaik dengan fungsi fitnes terbaik

        if (fit_global[0]<fit_baik[0]): #membandingkan fitnes terbaik global dengan fitnes terbaik lokal
            fit_global = fit_baik #menyimpan ke dalam fit_global jika fitnes baik jika lebih besar dari fit_global
            pop = pop_lokal
            fitbagus = hasil_fitlokalisasi  
        print("Generasi : ",i)
        i+=1
    krom_pilih = pop[fit_global[1]] #kromosom terpilih di tampung di variabel krom_pilih
    tamp= (split_krom(5)) #variabel tamp digunakan untuk menampung hasil menjadi 5 gen per rule
    terjemahan = decode(tamp) #melakukan decode dengan menerjemahkan integer ke dalam kalimat berdasarkan kromosom terbaik dengan memanggil fungsi decode
    uji = banding_uji(tamp) #melakukan uji antara data uji dengan kromosom terbaik yang di tampung di variabel uji

    with open('opsi_2.csv', 'w', newline='') as f: #untuk menulis kedalam csv berdasarkan data uji dengan kromosom terbaik 
        writer = csv.writer(f)
        writer.writerows(uji) #menyimpan uji (hasil keputusan) kedalam csv berupa file.csv dengan judul csvnya opsi_2.csv
 
    #melakukan print dari hasil yang sudah di dapakan 
    print('indeks kromosom      : ',fit_global[1])
    print('Nilai fitnes terbaik : ',fit_global[0])
    print('Kromosom terbaik     : ',pop[fit_global[1]])
    print('Hasil keputusan      : ',uji)
    print('Total generasi       : ',i-1)
    print('='*130)
    print('Dekode best kromosom : ',terjemahan)