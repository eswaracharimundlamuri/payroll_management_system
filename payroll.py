import oracledb
import boto3
import csv
from io import StringIO


class PayrollManagementSystem:

    def __init__(self):
        # Employee Data
        self.emp_ids = []
        self.emp_names = []
        self.emp_designations = []
        self.emp_salaries = []

        # Global rules
        self.pf_pct = 0
        self.cess_pct = 0

        # DB objects
        self.connection = None
        self.cursor = None

    # ---------------- ORACLE DB CONNECTION  ----------------
    def connect_oracle(self):
        try:
            self.connection = oracledb.connect(
                user="**",
                password="**",
                dsn=oracledb.makedsn(
                    "ec2-3-111-0-185.ap-south-1.compute.amazonaws.com",
                    1521,
                    service_name="ORCL"
                )
            )
            self.cursor = self.connection.cursor()
            print(" Connected to Oracle DB")
        except Exception as e:
            print("Oracle DB Connection Failed:", e)

    # ---------------- AWS S3 BUCKET ACCESS----------------
    def load_s3_data(self):
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id='****',
                aws_secret_access_key='*****',
                region_name='ap-south-1'
            )

            obj = s3.get_object(
                Bucket='payroll-project-team39',
                Key='Employee_details_1000.csv'
            )

            data = obj['Body'].read().decode('utf-8')
            reader = csv.reader(StringIO(data))
            next(reader)  # skip header

            for row in reader:
                self.emp_ids.append(row[0])
                self.emp_names.append(row[1])
                self.emp_designations.append(row[2])
                self.emp_salaries.append(float(row[3]))

            #print(" S3 Data Loaded")

        except Exception as e:
            print("S3 Connection Failed:", e)

    # ---------------- GLOBAL RULES  ----------------
    def load_global_rules(self):
        try:
            self.cursor.execute("SELECT rule_value FROM Global_Rules WHERE rule_name='pf_pct'")
            self.pf_pct = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT rule_value FROM Global_Rules WHERE rule_name='cess_pct'")
            self.cess_pct = self.cursor.fetchone()[0]

        except Exception as e:
            print(" Failed to load global rules:", e)

    # ---------------- SALARY PROCESS ----------------
    def process_employee(self, emp_name):
        try:
            # Check if employee already exists
            self.cursor.execute(
                "SELECT 1 FROM Employee_Master WHERE emp_name = :name",
                {"name": emp_name}
            )
            if self.cursor.fetchone():
                print("Employee already exists")
                return

            # Find employee in S3 data
            for i in range(len(self.emp_names)):
                if self.emp_names[i] == emp_name:
                    self.emp_id = self.emp_ids[i]
                    self.emp_name = self.emp_names[i]
                    self.designation = self.emp_designations[i]
                    self.basic_salary = self.emp_salaries[i]
                    break
            else:
                print(" Employee not found in S3")
                return

            self.load_designation_rules()
            self.calculate_gross()
            self.calculate_deductions()
            self.calculate_net()
            self.insert_data()

        except Exception as e:
            print(" Error processing employee:", e)

    # ---------------- DESIGNATION RULES ----------------
    def load_designation_rules(self):
        self.cursor.execute(
            "SELECT * FROM Designation_Rules WHERE designation = :d",
            {"d": self.designation}
        )
        self.rules = self.cursor.fetchone()

        if not self.rules:
            raise Exception(f"Designation rules not found for {self.designation}")

    # ---------------- CALCULATIONS ----------------
    def calculate_gross(self):
        self.hra = self.basic_salary * self.rules[1] / 100
        self.da = self.basic_salary * self.rules[2] / 100
        self.special = self.basic_salary * self.rules[3] / 100

        self.gross = self.basic_salary + self.hra + self.da + self.special

        '''print("\n------ Salary Breakdown ------")
        print(f"Basic: {self.basic_salary}")
        print(f"HRA: {round(self.hra, 2)}")
        print(f"DA: {round(self.da, 2)}")
        print(f"Special Allowance: {round(self.special, 2)}")
        print(f"Gross Salary: {round(self.gross, 2)}")'''

    def calculate_deductions(self):
        self.pf = self.basic_salary * self.pf_pct / 100
        self.tax = self.gross * self.rules[4] / 100
        self.cess = self.tax * self.cess_pct / 100

        self.total_deductions = self.pf + self.tax + self.cess

        '''print("\n------ Deductions ------")
        print(f"PF: {round(self.pf, 2)}")
        print(f"Tax: {round(self.tax, 2)}")
        print(f"Cess: {round(self.cess, 2)}")
        print(f"Total Deductions: {round(self.total_deductions, 2)}")'''

    def calculate_net(self):
        self.net = self.gross - self.total_deductions
        print(f"\nNet Salary of {self.emp_name}: {round(self.net, 2)}")


    def insert_data(self):
        self.cursor.execute(
            """
            INSERT INTO Employee_Master(emp_id, emp_name, designation, gross_salary, net_salary)
            VALUES (:1, :2, :3, :4, :5)
            """,
            (self.emp_id, self.emp_name, self.designation, self.gross, self.net)
        )

        self.cursor.execute(
            """
            INSERT INTO Salary_Details(
                salary_id, basic, hra, da, special_allowance,
                pf, cess, total_deductions, emp_id
            )
            VALUES (
                salary_seq_val.NEXTVAL, :1, :2, :3, :4,
                :5, :6, :7, :8
            )
            """,
            (
                self.basic_salary, self.hra, self.da, self.special,
                self.pf, self.cess, self.total_deductions, self.emp_id
            )
        )

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()



if __name__ == "__main__":

    system = PayrollManagementSystem()

    system.connect_oracle()
    system.load_s3_data()
    system.load_global_rules()

    while True:
        print("\n1. Enter Employee Name\n2. Exit")
        try:
            choice = int(input("Enter option: "))

            if choice == 1:
                name = input("Enter employee name: ")
                system.process_employee(name)

            elif choice == 2:
                break

            else:
                print("Invalid choice")

        except ValueError:
            print("Enter valid number")

    system.commit()
    system.close()