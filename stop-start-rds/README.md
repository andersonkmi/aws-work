### Start/stop automático de instâncias RDS

Os seguintes passos são necessários para configurar start e stop automático de instâncias RDS.

1. Criar uma custom policy no IAM que permitrá ao System Manager realizar operações no RDS. Rodar o comando abaixo:

    ```bash
    $ aws iam create-policy --policy-name StartStopRDSInstances --policy-document file://stop-start-rds-custom-policy.json --description "This policy grants access to start, stop and reboot all RDS instances in this account"
    ```

    A saída do comando acima deverá ser parecido o exemplo abaixo:
    ```json
    {
        "Policy": {
            "PolicyName": "StartStopRDSInstances",
            "PolicyId": "ANPA6DZNVLIZIGJS6REZL",
            "Arn": "arn:aws:iam::012345678901:policy/StartStopRDSInstances",
            "Path": "/",
            "DefaultVersionId": "v1",
            "AttachmentCount": 0,
            "PermissionsBoundaryUsageCount": 0,
            "IsAttachable": true,
            "CreateDate": "2024-10-13T11:13:23+00:00",
            "UpdateDate": "2024-10-13T11:13:23+00:00"
        }
    }
    ```

2. Criar uma nova role executando o comando abaixo:
    ```
    $ aws iam create-role --role-name start-stop-rds-instances-role --assume-role-policy-document file://trust-policy.json
    ```

    A saída do comando acima será similar ao exemplo abaixo:
    ```json
    {
        "Role": {
            "Path": "/",
            "RoleName": "start-stop-rds-instances-role",
            "RoleId": "AROA6DZNVLIZPFKPFMYXH",
            "Arn": "arn:aws:iam::012345678901:role/start-stop-rds-instances-role",
            "CreateDate": "2024-10-13T11:27:48+00:00",
            "AssumeRolePolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ssm.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
        }
    }
    ```

3. Associar a policy criado no passo 1 com a role criada no passo anterior. Executar o comando abaixo, substituindo o ARN da policy criada no passo 1.

    ```
    $ aws iam attach-role-policy --role-name start-stop-rds-instances-role --policy-arn arn:aws:iam::012345678901:policy/StartStopRDSInstances
    ```

4. Para cada instância RDS e dia da semana a ser configurada, executar o par de comandos abaixo:
    ```bash
    $ aws ssm create-association --name "AWS-StartRdsInstance" --parameters "InstanceId=codecraftlabs" --parameters '{"AutomationAssumeRole" : ["arn:aws:iam::012345678901:role/start-stop-rds-instances-role"], "InstanceId" : ["codecraftlabs"]}' --schedule-expression "cron(0 00 17 ? * SUN *)" --apply-only-at-cron-interval --association-name "rds-start-sun-schedule"
    ```

    ```bash
    $ aws ssm create-association --name "AWS-StopRdsInstance" --parameters "InstanceId=codecraftlabs" --parameters '{"AutomationAssumeRole" : ["arn:aws:iam::012345678901:role/start-stop-rds-instances-role"], "InstanceId" : ["codecraftlabs"]}' --schedule-expression "cron(0 00 18 ? * SUN *)" --apply-only-at-cron-interval --association-name "rds-stop-sun-schedule"
    ```

    Os seguintes parâmetros devem ser trocados de acordo com o ambiente:
    - ARN da role
    - InstanceId
    - Schedule expression: os horários são baseados em UTC
    - Association name
