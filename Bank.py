from tabulate import tabulate
import cx_Oracle
try:
            con=cx_Oracle.connect("system/VIVEK@localhost/xe")
            cur=con.cursor()
except Exception as e:
            print(e)
else:
            class Admin:
                        def closedAcc(self):
                                    cur.execute("SELECT * FROM VIVEK.printhistory")
                                    q=cur.fetchall()
                                    if q!=[]:
                                                print tabulate(q,headers=['Account No.','Date'])
                                    else:
                                                print("\nNo account history exists")

                        def restore_clsacc(self,custid):
                                    cur.execute("SELECT * FROM VIVEK.ret_cls WHERE customer_id=:1",{'1':custid})
                                    q=cur.fetchall()
                                    if q!=[]:
                                                cur.execute("""INSERT INTO  VIVEK.customer VALUES (:pram0,:pram1,:pram2,:pram3,:pram4,:pram5,:pram6,:pram7,:pram8,:pram9,:pram10,:pram11,:pram12,:pram13)""",(q[0][0],q[0][1],q[0][2],q[0][3],q[0][4],q[0][5],q[0][6],q[0][7],q[0][8],q[0][9],q[0][10],q[0][11],q[0][12],q[0][13]))
                                                con.commit()
                                                cur.execute("DELETE FROM VIVEK.ret_cls WHERE customer_id=:1",{'1':custid})
                                                con.commit()
                                                cur.execute("DELETE FROM VIVEK.printhistory WHERE account_no=:1",{'1':custid})
                                                con.commit()
                                                print("Account successfully restored")
                                    else:
                                                print("\nNo such Account exists")
            
            class Account:
                        def addressChange(self,custid,addr):
                                    cur.execute("""UPDATE VIVEK.customer SET address=:1 WHERE customer_id=:2""",{'1':addr,'2':custid})
                                    con.commit()
                                    print("Address changed successfully")
                                    
                        def makeDeposit(self,bal,accn):
                                    cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                    q=cur.fetchall()
                                    if q!=[]:
                                                bal1=q[0][0]+bal
                                                cur.execute("""UPDATE VIVEK.customer SET balance=:1 WHERE customer_id=:2""",{'1':bal1,'2':accn})
                                                con.commit()
                                                cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                q=cur.fetchall()
                                                print("\nDeposit Success\nCurrent balance: "+str(q[0][0]))
                                                cur.execute("""INSERT INTO VIVEK.printstatement VALUES (SYSDATE,:1,'Credit',:2,:3)""",{'1':accn,'2':bal,'3':bal1})
                                                con.commit()
                                    else:
                                                print("\nAccount No. does not exists")

                        def makeWithdrawal(self,bal,accn,custid):
                                    cur.execute("SELECT account_type FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                    acctyp=cur.fetchall()
                                    if acctyp!=[]:
                                                acctyp=acctyp[0][0]
                                                if accn==custid:
                                                            cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                            q=cur.fetchall()
                                                            if acctyp=='s':
                                                                        if q[0][0]<bal:
                                                                                    print("\nCannot withdraw. Current balance: "+str(q[0][0]))
                                                                        else:
                                                                                    bal1=q[0][0]-bal
                                                                                    cur.execute("""UPDATE VIVEK.customer SET balance=:1 WHERE customer_id=:2""",{'1':bal1,'2':accn})
                                                                                    con.commit()
                                                                                    cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                                                    q=cur.fetchall()
                                                                                    print("\nWithdrawal Success\nCurrent balance: "+str(q[0][0]))
                                                                                    cur.execute("INSERT INTO VIVEK.printstatement VALUES(SYSDATE,:1,'Debit',:2,:3)",(accn,bal,bal1))
                                                                                    con.commit()
                                                            if acctyp=='c':
                                                                        if q[0][0]<bal:
                                                                                    print("\nCannot withdraw. Current balance: "+str(q[0][0]))
                                                                        else:
                                                                                    bal1=q[0][0]-bal
                                                                                    if bal1>5000:
                                                                                                cur.execute("""UPDATE VIVEK.customer SET balance=:1 WHERE customer_id=:2""",{'1':bal1,'2':accn})
                                                                                                con.commit()
                                                                                                cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                                                                q=cur.fetchall()
                                                                                                print("\nWithdrawal Success\nCurrent balance: "+str(q[0][0]))
                                                                                                cur.execute("INSERT INTO VIVEK.printstatement VALUES(SYSDATE,:1,'Debit',:2,:3)",(accn,bal,bal1))
                                                                                                con.commit()
                                                                                    else:
                                                                                                print("\nCannot Withdraw. Minimum Balance required in account is: 5000")
                                                else:
                                                            print("\nWithdrawal from others account not possible. Check the Account No. and try again!")
                                    else:
                                                print("\nInvalid account no")

                        def transferMoney(self,bal,accn,custid):
                                    cur.execute("SELECT account_type FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                    acctyp=cur.fetchall()
                                    acctyp=acctyp[0][0]
                                    cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                    q=cur.fetchall()
                                    if q[0][0]<bal:
                                                print("\nCannot transfer. Current Balance: "+str(q[0][0]))
                                    else:
                                                bal1=q[0][0]-bal
                                                if acctyp=='s':
                                                            while True:
                                                                        print("\n1. Commit Transfer\n2. Rollback Transfer")
                                                                        ch=int(raw_input())
                                                                        if ch==1:
                                                                                    cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                                                    q=cur.fetchall()
                                                                                    if q!=[]:
                                                                                                cur.execute("""UPDATE VIVEK.customer SET balance=:1 WHERE customer_id=:2""",{'1':bal1,'2':custid})
                                                                                                con.commit()
                                                                                                cur.execute("INSERT INTO VIVEK.printstatement VALUES(SYSDATE,:1,'Debit',:2,:3)",(custid,bal,bal1))
                                                                                                con.commit()
                                                                                                cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                                                                q=cur.fetchall()
                                                                                                bal1=q[0][0]+bal
                                                                                                cur.execute("""UPDATE VIVEK.customer SET balance=:1 WHERE customer_id=:2""",{'1':bal1,'2':accn})
                                                                                                con.commit()
                                                                                                cur.execute("INSERT INTO VIVEK.printstatement VALUES(SYSDATE,:1,'Credit',:2,:3)",(accn,bal,bal1))
                                                                                                con.commit()
                                                                                                cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                                                                                q=cur.fetchall()
                                                                                                #cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn}))
                                                                                                #q1=cur.fetchall()
                                                                                                print("\nTransfer Success\nCurrent Balance: "+str(q[0][0]))
                                                                                                break;
                                                                                    else:
                                                                                                print("\nInvalid Account No: "+str(accn))
                                                                                                break;
                                                                        elif ch==2:
                                                                                    print("\nTransfer Cancelled")
                                                                                    break;
                                                                        else:
                                                                                    print("Wrong input. Try again!")
                                                if acctyp=='c':
                                                            if bal1>5000:
                                                                        while True:
                                                                                    print("\n1. Commit Transfer\n2. Cancel Transfer")
                                                                                    ch=int(raw_input())
                                                                                    if ch==1:
                                                                                                cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                                                                q=cur.fetchall()
                                                                                                if q!=[]:
                                                                                                            cur.execute("""UPDATE VIVEK.customer SET balance=:1 WHERE customer_id=:2""",{'1':bal1,'2':custid})
                                                                                                            con.commit()
                                                                                                            cur.execute("INSERT INTO VIVEK.printstatement VALUES(SYSDATE,:1,'Debit',:2,:3)",(custid,bal,bal1))
                                                                                                            con.commit()
                                                                                                            cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn})
                                                                                                            q=cur.fetchall()
                                                                                                            bal1=q[0][0]+bal
                                                                                                            cur.execute("""UPDATE VIVEK.customer SET balance=:1 WHERE customer_id=:2""",{'1':bal1,'2':accn})
                                                                                                            con.commit()
                                                                                                            cur.execute("INSERT INTO VIVEK.printstatement VALUES(SYSDATE,:1,'Credit',:2,:3)",(accn,bal,bal1))
                                                                                                            con.commit()
                                                                                                            cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                                                                                            q=cur.fetchall()
                                                                                                            #cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':accn}))
                                                                                                            #q1=cur.fetchall()
                                                                                                            print("\nTransfer Success\nCurrent Balance: "+str(q[0][0]))
                                                                                                            break;
                                                                                                else:
                                                                                                            print("\nInvalid Account No: "+str(accn))
                                                                                                            break;
                                                                                    elif ch==2:
                                                                                                print("\nTransfer Cancelled")
                                                                                                break;
                                                                                    else:
                                                                                                print("Wrong input. Try again!")
                                                            else:
                                                                        print("\nCannot Transfer. Minimum Balance required in account is: 5000")
                                                                        
                                                
                        def display(self,custid):
                                    cur.execute("select * from VIVEK.printstatement WHERE customer_id=:1 order by customer_id,Account_Date",{'1':custid})
                                    qury=cur.fetchall()
                                    print tabulate(qury,headers=['Date','Account No.','Transaction type','Amount','Balance'])

                        def accountCls(self,custid):
                                    cur.execute("INSERT INTO VIVEK.printhistory VALUES(:1,SYSDATE)",{'1':custid})
                                    con.commit()
                                    cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                    q=cur.fetchall()
                                    cur.execute("SELECT address,city,state,pincode FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                    q1=cur.fetchall()
                                    print("\nYour Amount: "+str(q[0][0])+" will be sent to the address: "+q1[0][0]+","+q1[0][1]+","+q1[0][2]+","+str(q1[0][3]))
                                    cur.execute("SELECT *FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                    q=cur.fetchall()
                                    cur.execute("""INSERT INTO  VIVEK.ret_cls VALUES (:pram0,:pram1,:pram2,:pram3,:pram4,:pram5,:pram6,:pram7,:pram8,:pram9,:pram10,:pram11,:pram12,:pram13)""",(q[0][0],q[0][1],q[0][2],q[0][3],q[0][4],q[0][5],q[0][6],q[0][7],q[0][8],q[0][9],q[0][10],q[0][11],q[0][12],q[0][13]))
                                    con.commit()
                                    cur.execute("DELETE FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                    con.commit()
                                    print("Account closed successfully")
                        
            class Customer:

                        def signUp(self,acctyp,name,gender,mob,addr,state,city,pincode,email,password,balance):
                                    cur.execute("""INSERT INTO  VIVEK.customer VALUES (VIVEK.C_ID_VAL.NEXTVAL,:pram0,:pram1,:pram2,:pram3,:pram4,:pram5,:pram6,:pram7,:pram8,:pram9,:pram10,'0',SYSDATE)""",(acctyp,name,gender,mob,addr,state,city,pincode,email,password,balance))
                                    con.commit()
                                    cur.execute("SELECT max(customer_id) FROM VIVEK.customer")
                                    q=cur.fetchall()
                                    cur.execute("UPDATE VIVEK.customer SET Account_No=:1 Where customer_id=:1",{'1':q[0][0]})
                                    print("\nYou have successfully signed up")
                                    con.commit()
                                    cur.execute("INSERT INTO VIVEK.printstatement VALUES(SYSDATE,:1,'Credit',:2,:2)",{'1':q[0][0],'2':balance})
                                    con.commit()
                                    print("\nYour Customer Id and Account Number is: "+str(q[0][0]))
                        def signIn(self,custid,psswd):
                                    accnt=Account();
                                    cur.execute("SELECT password FROM VIVEK.customer WHERE customer_id=:1",{'1':custid})
                                    q=cur.fetchall()
                                    if q!=[]:
                                                if psswd==q[0][0]:
                                                            print("\nSigned In Successful")
                                                            while True:
                                                                        print("""\n1. Address Change\n2. Money Deposit\n3. Money Withdrawal\n4. Print Statemant\n5. Transfer Money\n6. Account Closure\n7.Customer logout""")
                                                                        ch=int(raw_input())
                                                                        if ch==1:
                                                                                    accnt.addressChange(custid,raw_input("Enter the new Address"))
                                                                        elif ch==2:
                                                                                    accnt.makeDeposit(int(raw_input("Enter Balance: ")),int(raw_input("Enter account no.")))
                                                                        elif ch==3:
                                                                                    accnt.makeWithdrawal(int(raw_input("Enter Balance: ")),int(raw_input("Enter account no.")),custid)
                                                                        elif ch==4:
                                                                                    accnt.display(custid)
                                                                        elif ch==5:
                                                                                    accnt.transferMoney(int(raw_input("Enter Balance: ")),int(raw_input("Enter account no.")),custid)
                                                                        elif ch==6:
                                                                                    accnt.accountCls(custid)
                                                                                    break;
                                                                        elif ch==7:
                                                                                    break;
                                                                        else:
                                                                                    print("Wrong choice. Try Again!")
                                                            return 1;
                                                else:
                                                            print("\nInvalid Password")
                                    else:
                                                return 0;
                                    
                                                

                        def adminSignIn(self,adid,psswd):
                                    cur.execute("SELECT password FROM VIVEK.admin WHERE admin_id=:1",{'1':adid})
                                    q=cur.fetchall()
                                    if q!=[]:
                                                if psswd==q[0][0]:
                                                            print("\nSigned In Successful")
                                                            while True:
                                                                        print("\n1. Print closed Accounts History\n2. Restore closed account\n3. Admin Logout\n")
                                                                        ch=int(raw_input())
                                                                        if ch==1:
                                                                                    Admin().closedAcc()
                                                                        elif ch==2:
                                                                                    custid=int(raw_input("\nEnter the account no. which you want to restore: "))
                                                                                    Admin().restore_clsacc(custid)
                                                                        elif ch==3:
                                                                                    break;                                                                                    
                                                                        else:
                                                                                    print("Wrong choice. Try Again!")
                                                            return 1;
                                                else:
                                                            print("\nInvalid Password")
                                    else:
                                                return 0;
                        
            class Switch:
                        def __init__(self,num):
                                    self.num=num
                        def options(self):
                                    custobj=Customer()
                                    if self.num==1:
                                                while True:
                                                            self.acctyp=raw_input("Account Type('s' for Savings account, 'c' for Current account): ")
                                                            if self.acctyp=='s' or self.acctyp=='c':
                                                                        break;
                                                            else:
                                                                        print("\nNo such account exists. Try again!")
                                                while True:
                                                            if self.acctyp=='c':
                                                                        self.bln=int(raw_input("Enter Balance"))
                                                                        if self.bln<5000:
                                                                                    print("Minimum balance required to open current account is: 5000. Enter again!")
                                                                        else:
                                                                                    break;
                                                            if self.acctyp=='s':
                                                                        print("1. Enter balance\n2. Skip and Continue")
                                                                        self.ch=int(raw_input())
                                                                        if self.ch==1:
                                                                                    self.bln=int(raw_input("Enter Balance"))
                                                                                    break;
                                                                        elif self.ch==2:
                                                                                    self.bln=0
                                                                                    break;
                                                                        else:
                                                                                    print("Wrong input. Try Again!")
                                                self.name=raw_input("Full Name: ")
                                                while True:
                                                            self.gender=raw_input("Gender('m' for Male, 'f' for Female: ")
                                                            if self.gender=='m' or self.gender=='f':
                                                                        break;
                                                            else:
                                                                        print("\nWrong input. Try again!")
                                                self.mob=int(raw_input("Mobile No.: "))
                                                self.addr=raw_input("Address: ")
                                                self.state=raw_input("State: ")
                                                self.city=raw_input("City: ")
                                                while True:
                                                            self.pincode=int(raw_input("Pincode: "))
                                                            if (len(str(self.pincode)))==6:
                                                                break;
                                                            else:
                                                                print("\nPincode should not be less than 6 digits")
                                                self.email=raw_input("Email: ")
                                                while True:
                                                            self.__password=raw_input("\nPassword(minimum 8 characters): ")
                                                            if len(self.__password)>=8:
                                                                        break;
                                                            else:
                                                                        print("\nPassword should not be less than 8 characters")
                                                custobj.signUp(self.acctyp,self.name,self.gender,self.mob,self.addr,self.state,self.city,self.pincode,self.email,self.__password,self.bln)
                                    elif self.num==2:
                                                c=3;
                                                while True:
                                                            if c>=1 and c<=3:
                                                                        self.customerId=int(raw_input("Customer Id: "))
                                                                        self.__password=raw_input("Password: ")
                                                            else:
                                                                        print("\nYour account is locked")
                                                                        cur.execute("SELECT balance FROM VIVEK.customer WHERE customer_id=:1",{'1':self.customerId})
                                                                        q=cur.fetchall()
                                                                        cur.execute("SELECT address,city,state,pincode FROM VIVEK.customer WHERE customer_id=:1",{'1':self.customerId})
                                                                        q1=cur.fetchall()
                                                                        print("\nYour Amount: "+str(q[0][0])+" will be sent to the address: "+q1[0][0]+","+q1[0][1]+","+q1[0][2]+","+str(q1[0][3]))
                                                                        cur.execute("DELETE FROM VIVEK.customer WHERE customer_id=:1",{'1':self.customerId})
                                                                        con.commit()
                                                                        break;
                                                            rtn=custobj.signIn(self.customerId,self.__password);
                                                            if rtn==1:
                                                                        break;
                                                            elif rtn==0:
                                                                        print("\nNo such account exists")
                                                                        break;
                                                            else:
                                                                        print("\n"+str(c-1)+"trials left")
                                                                        c-=1;

                                    elif self.num==3:
                                                c=3;
                                                while True:
                                                            if c>=1 and c<=3:
                                                                        self.customerId=int(raw_input("Customer Id: "))
                                                                        self.__password=raw_input("Password: ")
                                                            else:
                                                                        print("\nYour account is locked")
                                                                        cur.execute("DELETE FROM VIVEK.admin WHERE customer_id=:1",{'1':self.customerId})
                                                                        con.commit()
                                                                        break;
                                                            rtn=custobj.adminSignIn(self.customerId,self.__password);
                                                            if rtn==1:
                                                                        break;
                                                            elif rtn==0:
                                                                        print("\nNo such account exists")
                                                                        break;
                                                            else:
                                                                        print("\n"+str(c-1)+"trials left")
                                                                        c-=1;

                                    elif self.num==4:
                                                con.close()
                                                exit()

                                    else:
                                                print("\nInvalid choice\nTry again\n")


            while True:
                        print("\n1. Sign Up(New Customer)\n2. Sign In(Existing Customer)\n3. Admin Sign In\n4. Quit")
                        try:
                                    n=int(raw_input())
                        except Exception as e:
                                    print(e)
                        else:
                                    sw=Switch(n)
                                    sw.options()
