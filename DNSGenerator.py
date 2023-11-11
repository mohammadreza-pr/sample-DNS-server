import re

hosts = {}


def load_records():
    global hosts
    hosts_file = open('hosts', 'r')
    for line in hosts_file:
        if line[0] != '#':
            IP, domain = line.split('\t')
            if line.endswith('\n'):
                domain = domain[:-1]
            if hosts.keys().__contains__(domain):
                records = hosts.get(domain)
                records.append(IP)
                hosts[domain] = records
            else:
                hosts[domain] = [IP]


load_records()


def extract_domain_record(domain):
    global hosts
    if hosts.keys().__contains__(domain):
        return hosts.get(domain)
    else:
        return []


class DNSGenerator:
    def __init__(self, data):
        self.data = data
        self.format_error = 0
        self.current_index_of_input = 0
        self.QR = '1'
        self.OPCODE = None
        self.AA = '1'
        self.TC = '0'
        self.RD = '0'
        self.RA = '0'
        self.Z = '000'
        self.RCODE = None
        self.QDCOUNT = b'\x00\x01'
        self.NSCOUNT = b'\x00\x00'
        self.ARCOUNT = b'\x00\x00'
        self.domain = None

    def extract_question_type(self):
        self.current_index_of_input += 2

    def extract_domain_name(self):
        self.current_index_of_input = 12
        try:
            self.check_if_question_is_empty()
            labels = []
            while self.data[self.current_index_of_input] != 0:
                label = self.extract_one_label()
                labels.append(label)
            self.current_index_of_input += 1
            self.domain = '.'.join(labels)
        except IndexError:
            self.domain = ''

    def extract_one_label(self):
        number_of_chars = self.data[self.current_index_of_input]
        label = ''
        for i in range(number_of_chars):
            new_char = chr(self.data[self.current_index_of_input + i + 1])
            label = label + new_char
        self.current_index_of_input += number_of_chars + 1
        return label

    def run(self):
        records = self.extract_record()
        response = self.create_response(records)
        return response

    def extract_record(self):
        self.extract_domain_name()
        self.extract_question_type()
        self.extract_class_type()
        records = extract_domain_record(self.domain)
        return records

    def check_if_question_is_empty(self):
        question_count = self.data[3:5]
        if question_count == 0:
            raise IndexError

    def create_response(self, records):
        header = self.create_response_header(records)
        question = self.create_response_question()
        answer = self.make_response_answer(records)
        return header + question + answer

    def create_response_question(self):
        return self.data[12:self.current_index_of_input]

    def create_response_header(self, records):
        ID = self.extract_query_id()
        flags = self.create_flags(records)
        ANCOUNT = len(records).to_bytes(2, byteorder='big')
        return ID + flags + self.QDCOUNT + ANCOUNT + self.NSCOUNT + self.ARCOUNT

    def extract_query_id(self):
        return self.data[:2]

    def generate_opcode(self):
        opcode_byte = self.data[2:3]
        self.OPCODE = ''
        for bit in range(1, 5):
            self.OPCODE += str(ord(opcode_byte) & (1 << bit))

    def create_flags(self, records):
        self.generate_opcode()
        first_byte = int(self.QR + self.OPCODE + self.AA + self.TC + self.RD, 2).to_bytes(1, byteorder='big')
        self.generate_response_code(records)
        second_byte = int(self.RA + self.Z + self.RCODE, 2).to_bytes(1, byteorder='big')
        return first_byte + second_byte

    def generate_response_code(self, records):
        if len(records) == 0:
            self.RCODE = '0003'
        else:
            self.RCODE = '0000'

    def make_response_answer(self, records):
        answer = b''
        for record in records:
            answer += self.data[12:self.current_index_of_input]
            answer += int(400).to_bytes(4, byteorder='big')
            answer += b'\x00\x04'
            for part in record.split('.'):
                answer += bytes([int(part)])

        return answer

    def extract_class_type(self):
        self.current_index_of_input += 2
