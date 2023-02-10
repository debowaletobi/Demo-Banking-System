from  datetime import datetime, timezone, timedelta

class Timezone:
    
    def __init__(self, name:str, hours_offset:int, minutes_offset:int):
        if name is None or len(str(name.strip()))==0:
            raise ValueError("Timezone name cannot be empty")
            
        if isinstance(name,str)==False:
            raise ValueError("Timezone name must be of type str")  
            
        self._name = name
        if isinstance(hours_offset,int)==False or isinstance(minutes_offset,int)==False:
            raise ValueError("Offset value must be an integer")
            
        if minutes_offset < -59 or minutes_offset > 59:
            raise ValuError("minutes offset must be between -59 and 59")
        self._minutes_offset = minutes_offset
        
        offset = timedelta(hours=hours_offset, minutes=minutes_offset)
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0): 
            raise ValueError("Hour Offset must be between -12 and 14")
        self._hours_offset = hours_offset
        
        self._offset = offset
        
    @property
    def offset(self) -> timedelta:
        return self._offset
    
    @property
    def name(self) -> str:
        return self._name 
    
    def __eq__(self,other) -> bool:
        return (isinstance(other,Timezone)
               and self.name==other.name
               and self.offset == other.offset)
    
    def __repr__(self) -> str:
        return (f"Timezone: {self._name}"
                f"\nHours Offset: {self._hours_offset}"
                f"\nMinutes Offset: {self._minutes_offset}")


class Account:
    
    accounts = []
    transaction_codes = {'deposit':'D','decline':'X',
                         'interest deposit':'I',
                         'withdrawal':'W'}
    transactions_data = {}
    monthly_interest_rate = 0.02
    transaction_id = 0
    
    def __init__(self, account_no:int, first_name:str, last_name:str, timezone:Timezone=utc):
        
        account_no = str(account_no)
        self._account_no = Account.validate_account(account_no)
        
        self._first_name = Account.validate_name(first_name,"First name")

        self._last_name =  Account.validate_name(last_name, "Last name")
        
        self._full_name = None

        self._transaction_count = 0
        self._time_zone = timezone
        self._balance = 0
   

    @classmethod    
    def validate_account(cls,account_no)->str:
        if account_no in cls.accounts:
            raise ValueError("Duplicate account")
        if isinstance(account_no,int): 
            raise ValueError("Account must consist of all numbers")
        if len(account_no)!=2:
            raise ValueError("Account must be two numbers long")
        cls.accounts.append(account_no)
        return account_no
       
        
    @staticmethod
    def validate_name(name, name_type):
        if not isinstance(name,str):
            raise ValueError(f"{name_type} must be a string")
        if not len(str(name).strip()) > 0:
            raise ValueError(f"{name_type} can not be empty")
        return (str(name).strip())
        
        
    @property
    def account_no(self) -> str:
        return self._account_no
    
    
    @property
    def first_name(self) -> str:
        return self._first_name
    
    
    @property
    def last_name(self) -> str:
        return self._last_name
    
    
    @first_name.setter
    def first_name(self,name):
        self.validate_name(name,"First name")
        self._first_name = name
        self._full_name = None
        
        
    @last_name.setter
    def last_name(self,name):
        self.validate_name(name,"Last name")
        self._last_name = name
        self._full_name = None
    
    
    @property
    def full_name(self) -> str:
        if self._full_name is None:
            self._full_name = f"{first_name} {last_name}"
        return self._full_name

    
    @property
    def timezone(self) -> str:
        return self._time_zone.name
    
    
    @timezone.setter
    def timezone(self,timezone):
        if not isinstance(timezone,Timezone):
            raise ValueError("time zone must be of type Timezone")
        self._time_zone = timezone
    
    @property
    def balance(self):
        return self
    
    
    @staticmethod
    def _get_utc_time():
        return datetime.utcnow()
  

    def _get_user_time(self):
        return (datetime.utcnow() + self._time_zone.offset)
        
        
    @classmethod
    def get_transaction_info(cls, confirmation_no):
        return cls.transactions_data[confirmation_no]
        
        
    @classmethod
    def _generate_confirmation_no(cls, transaction_type, user_time, account_no,):
        code = Account.transaction_codes[transaction_type]
        utc_time = cls._get_utc_time()
        confirmation_no = f"{code}-{account_no}-{utc_time}-{cls.transaction_id}"
        cls.transactions_data[confirmation_no] = {'Account Number':account_no,
                                                 'Transaction Code':code,
                                                 'User Time':f"{user_time}",
                                                 'UTC Time':f"{utc_time}",
                                                 'Transaction ID':cls.transaction_id}
        cls.transaction_id += 1
                
        
    def deposit(self, amount):
        self._generate_confirmation_no('deposit',self._get_user_time(), self.account_no)
        self._balance += amount
        self._transaction_count += 1
        
        
    def withdraw(self, amount) -> float:
        if amount > self._balance:
            self._generate_confirmation_no('decline',self._get_user_time(), self.account_no)
            self._transaction_count += 1
            raise ValueError("Withdrawal amount greater than balance ")
        else:
            self._generate_confirmation_no('withdrawal',self._get_user_time, self.account_no)
            self._balance -= amount
            self._transaction_count += 1
            return amount
   

