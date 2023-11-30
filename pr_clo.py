import random
import time
import sys
import keyboard
import threading

#govira8011@dvdoto.com 12342334 https://mainnet.infura.io/v3/86083802b24040e5a3ba13dde2e4f901
#testkorob@mail.ru !1234Af2334 https://mainnet.infura.io/v3/6d734b115f6749b99a7e367bae83b29d
#korede9992@labebx.com 12342334 https://mainnet.infura.io/v3/23f22066d6d2459584f76f800caf1f30
hran=('https://www.ethercluster.com/etc','https://blockscout.com/etc/mainnet/api/')
hran_id=0

from web3 import Web3,  IPCProvider
#w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/6d734b115f6749b99a7e367bae83b29d'))
#w3 = Web3(Web3.HTTPProvider(hran[hran_id]))
w3 = Web3(Web3.IPCProvider("/clo/geth.ipc"))

l_adr = set()
q_s=False

def trans(n):
	global l_adr
	global w3
#	print("тр ",n)
	w1=w3.eth.get_transaction(n)
	l_adr.add(w1['from'])
	l_adr.add(w1['to'])
#	print("почикали тр ",n)

def adr_in_bl(bl_num):	#извлекаем транзакции из блока
	try:
		global l_adr
		global w3		
		w=w3.eth.get_block(bl_num)['transactions']
		print("блок ",coin," №", bl_num, "тр: ",len(w))		
		
		thr_trans=[]
		for i in range(len(w)):
			thr_trans_t=threading.Thread(target=trans, args=[w[i].hex()])
			thr_trans_t.start()
			thr_trans.append(thr_trans_t)
			
		for thr_trans_t in thr_trans:
			thr_trans_t.join()
		#print ("длина потоков тран",len(thr_trans))
	
#		for i in range(len(w)):
		#print(w[i].hex())
#			w1=w3.eth.get_transaction(w[i].hex())
		#	print(w3.fromWei(w3.eth.get_balance(w1['from']),'ether'))
#			l_adr.add(w1['from'])
#			l_adr.add(w1['to'])
		
		#print(bl_num,"исполнен")
	except Exception:
		print("произошла ошибка сети, ждём 10 секунд...")
		time.sleep(10)
		global hran_id
		
		if (hran_id<(len(hran)-1)):
			hran_id+=1
		else:
			hran_id=0
		print("hran:",hran, " hran_id:",hran_id)
		print("hran{hran_id}-",hran[hran_id])
		
#		w3 = Web3(Web3.HTTPProvider(hran[hran_id]))
		adr_in_bl(bl_num)
		
def zap_blocks():
	f=open("blocks.txt","a")
	f.write("\n"+str(block-1))
	f.close()
		
def zap_adr_file():
	f = open('adr.txt',"at")
	for index in l_adr:
		f.write(str(index)+"\n")
	f.close()
	
def save_quit():
	global q_s
	q_s=True
	#print("gjgg")

def print_pressed_keys(e):	
    print(e, e.event_type, e.name)

def foo():
	print("gjgg")

f = open('blocks.txt',"rt")
for line in f:
	print(line)
f.close()

keyboard.add_hotkey('Ctrl + 0', save_quit)
		
start_time = time.time()
block=int(line)

threads=[]

kol_potok=50
block_max=6999999
block_max=w3.eth.get_block('latest')['number']
print('latest block ',block_max)
stop_mem=262253
coin="clo"
#block=1000000
#for i in range(100):	
while 1==1 :
	if (block>=block_max):
		print("достигли максимума")
		zap_adr_file()
		zap_blocks();
		exit()
	bk=block+kol_potok
	if (bk>block_max):
		kol_potok=block_max-block+1
		
	print(coin," от ", block," до ", block+kol_potok)
	for i in range(kol_potok):
		thr=threading.Thread(target = adr_in_bl, args = [block])
		thr.start()
		block+=1
		threads.append(thr)
	
	print("ждём пока отработают ",len(threads)," потоков")

	for t in threads:
		t.join()
	threads=[]
#	adr_in_bl(block)
	print("размер списка ",sys.getsizeof(l_adr))
	#print("закончили обрабатывать блок №", block)
#	block+=1
	
	#print(str(q_s)," i=",i)
	
	if ((sys.getsizeof(l_adr))>stop_mem):
		print("переполнилась память: размер блока = ",sys.getsizeof(l_adr))
		zap_adr_file()
		zap_blocks();
		l_adr=set()
		#i=0
		#break
	if (q_s==True):
		print("остановленно принудительно")			
		zap_adr_file()
		zap_blocks();
		exit()
	
		
print("1--- %s seconds ---" % (time.time() - start_time))

zap_blocks ()

print("dlina l_adr",len(l_adr))


print("dlina l_adr",len(l_adr))


 
print('размер множества',((sys.getsizeof(l_adr))/1024)/1024)

print(w3.eth.get_block(12194476)['transactions'][159].hex())
print(len(w3.eth.get_block(12194476)['transactions']))
print("транзакции от",w3.eth.get_transaction(w3.eth.get_block(12194476)['transactions'][0].hex())['from'])
print("транзакции к",w3.eth.get_transaction(w3.eth.get_block(12194476)['transactions'][0].hex())['to'])

#print(w3.eth.accounts.privateKeyToAccount('0x348ce564d427a3311b6536bbcff9390d69395b06ed6c486954e971d960fe8709'))
#pr_key = random.randint(0,2**256)
print(' -- ')


