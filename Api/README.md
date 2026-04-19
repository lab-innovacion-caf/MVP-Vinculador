## azfun-POC-VINCULADOR-CR

### Description

Backend for vinculador with azure function

### Requirements for run in local

- Python 3.10.15
- Pip 23.0.1
- Git

### Steps for run in local

1. Clone project with

```
git clone https://CAFrepos@dev.azure.com/CAFrepos/Innovation%20Lab/_git/Caf-vinculador-api
```

2. Go to project directory

```
cd azfun-POC-VINCULADOR-CR
```

3. Create virtual env

```
python3 -m venv venv
```

4. Activate virtual env

```
source venv/bin/activate
```

5. Install dependencies

```
pip3 install -r requirements.txt
```

6. Run project in port 3001

```
func start -p 3001 --verbose
```

command for deactivate virtual env

```
deactivate
```

command for list dependencies

```
pip3 list
```

### Commands for create new azure function in local and deploy

create azure function in local

```
func init azfun-POC-VINCULADOR-CR --python
```

start in local with the command:

```
func start -p 3001 --verbose
```

deploy with command

```
func azure functionapp publish azfun-POC-ESG-CR
```
