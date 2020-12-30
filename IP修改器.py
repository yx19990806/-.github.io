import wmi
import random
import tkinter as tk
window = tk.Tk()
window.title('IP修改器')
window.geometry('500x300')

var = tk.StringVar()
l = tk.Label(window, textvariable=var,bg='green',fg='white',font=('Arial',12),width=30,height=2)
l.pack()

t = tk.Entry(window)
t.pack()


def hit_me():
    m = t.get()
    print(m)
    arrIPAddresses=m.split()

    a = str(int(m[8]))
    b = str(int(m[9])+1)
    c = str(10)+'.'+str(255)+'.'+str(2)+a+b+'.'+str(254)
    arrDefaultGateways=c.split()

    print ('正在修改IP,请稍候...')

    wmiService = wmi.WMI()

    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)

    if len(colNicConfigs) < 1:

        print ('没有找到可用的网络适配器')



    for i in range(len(colNicConfigs)):

        print (str(i+1)+" : ",colNicConfigs[i].IPAddress)

        print ("-------------------------------------------------------\n")

    i=1

    objNicConfig = colNicConfigs[i-1]

    i=1

    if(i==1):

        #10.255.208.169
        #a = str(int(m[8]))
        #b = str(int(m[9])+1)
        #c = str(10)+'.'+str(255)+'.'+str(2)+a+b+'.'+str(254)
        arrSubnetMasks = ['255.255.254.0']
        #arrDefaultGateways = c.split()
        #arrDefaultGateways = ['10.255.2ab.254']


        arrGatewayCostMetrics = [1]
        arrDNSServers = ['10.0.9.88', '10.0.9.11']

        intReboot = 0

        returnValue = objNicConfig.EnableStatic(IPAddress = arrIPAddresses, SubnetMask =arrSubnetMasks)

        if returnValue[0] == 0 or returnValue[0] == 1:

            print ('设置IP成功')

            intReboot += returnValue[0]

        else:

            print ('修改失败: IP或子网掩码设置发生错误')

        returnValue = objNicConfig.SetGateways(DefaultIPGateway = arrDefaultGateways, GatewayCostMetric = arrGatewayCostMetrics)

        if returnValue[0] == 0 or returnValue[0] == 1:

            print ('设置网关成功')

            intReboot += returnValue[0]

        else:

            print ('修改失败: 网关设置发生错误')

        returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder = arrDNSServers)

        if returnValue[0] == 0 or returnValue[0] == 1:

            print ('设置DNS成功')

            intReboot += returnValue[0]

        else:

            print (str(returnValue)+'修改失败: DNS设置发生错误')




        if intReboot > 0:

            print ('需要重新启动计算机')

            print ('修改结束')

b = tk.Button(window, text='点击修改',font=('Arial,12'),width=10,height=1,command=hit_me)
b.pack()

window.mainloop()