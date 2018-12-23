from WhatsappFileReader import WhatsappFileReader
from pprint import pprint

for parse in WhatsappFileReader().process_files():
    title = parse['title']
    json = parse['json']
    file_to_move = parse['file_to_move']
    file_to_delete = parse['file_to_delete']
    path = parse['path']
    device = parse['device']

    print('')

