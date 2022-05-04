# What it is
hibpwn_check runs mass e-mail through Have I Been Pwned and output the result in xls format.<br>
The result indicates whether the e-mail has been pwned and the breach it was in. 
# Setup
```
git clone https://github.com/1oftheguthakrs/hibpwn_check.git
cd hibpwn_check
pip3 install -r requirements.txt
```
# Example
./hibpwn_check.py -f email.txt -p API_key 

# Credit
Much of the code was from Sq00ky's LeetLinked
https://github.com/Sq00ky/LeetLinked
