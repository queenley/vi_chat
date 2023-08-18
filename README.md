# Chatbot in Vietnamese
## Installation
Run this command
```
pip install -r requirements.txt
```
## Prepare dataset
### Translate
* Use ChatGPT API to translate SGD-DSTC8 dataset to Vietnamese 
Run this command
```
python src/data/translate/translate.py <openai_key> <data_url> <number_of_dialog> <save_path>
```
usage: Vietnamese Dialog Translation [-h] --key KEY [--repo_url REPO_URL] [--num NUM] [--save_path SAVE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --key KEY             the private key of ChatGPT API (default: None)
  --repo_url REPO_URL   the url contains all dataset (default: https://raw.githubusercontent.com/google-research-datasets/dstc8-schema-guided-dialogue/master/test/)
  --num NUM             the number of urls (default: 34)
  --save_path SAVE_PATH
                        the path to save (default: ./dataset/)
### Generate
* Use ChatGPT API to generate dataset
Run this command 
```
python src/data/generation/generate.py <arguments>
```
usage: Vietnamese Dialog Generation [-h] --key KEY [--domain DOMAIN] [--domain_type DOMAIN_TYPE] [--example EXAMPLE] [--user_action USER_ACTION] [--system_action SYSTEM_ACTION] [--slot SLOT] [--intent INTENT] [--num_dialog NUM_DIALOG] [--list_product LIST_PRODUCT] [--save_path SAVE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --key KEY             the private key of ChatGPT API (default: None)
  --domain DOMAIN       the domain of dialog (default: Flight)
  --domain_type DOMAIN_TYPE
                        the domain type of dialog. (service, trading, ...) (default: booking)
  --example EXAMPLE     the example dialog (default: ['USER: Xin chào, tôi chán quá', 'SYSTEM: Xin chào, tôi sẵn sàng ở đây để trò chuyện cùng bạn.', 'USER: Tôi muốn thực hiện chuyến du lịch từ Thành phố Hồ Chí Minh đến Đà Lạt. Tôi cần 2 vé một chiều vào thứ ba tuần sau. ', 'SYSTEM: Có một chuyến bay khởi hành lúc 5:00
                        sáng, không có điểm dừng, với mức phí là 1.000.000 VNĐ cho 1 người. ', 'USER: Tôi sẽ đến Đà Lạt vào lúc mấy giờ? ', 'SYSTEM: Khoảng 6:00 sáng bạn sẽ đến Đà Lạt. ', 'USER: Tuyệt vời, chuyến bay này rất phù hợp với tôi. ', 'SYSTEM: Bạn còn cần thêm yêu cầu gì nữa không? ', 'USER: Đây là lần đầu tiên
                        tôi đến Đà Lạt. Bạn có thể nói một chút về Đà Lạt cho tôi biết không? ', 'SYSTEM: Đà Lạt là một thành phố thuộc tỉnh Lâm Đồng, nằm trên cao nguyên Lâm Viên, thuộc vùng Tây Nguyên, Việt Nam. Thành phố Đà Lạt có một khí hậu miền núi dịu mát ôn hòa quanh năm. USER: cảm ơn', 'SYSTEM: không có chi, chúc
                        bạn có chuyên đi vui vẻ'])
  --user_action USER_ACTION
                        the list of user actions (default: ['INFORM', 'REQUEST', 'SELECT', 'CONFIRM', 'REQUEST-ALTS', 'BYE', 'GREET', 'BOOK', 'NOBOOK', 'OFFERBOOK', 'ASK', 'INFORM-INTENT', 'NEGATE-INTENT', 'AFFIRM-INTENT', 'AFFIRM', 'NEGATE', 'THANK'])
  --system_action SYSTEM_ACTION
                        the list of system actions (default: ['INFORM', 'REQUEST', 'SELECT', 'CONFIRM', 'OFFER', 'NoOFFER', 'RECOMMEND', 'PROMOTION_INTRODUCTION', 'NOTIFY_SUCCESS', 'NOTIFY_FALIURE', 'INFORM_COUNT', 'OFFER_INTENT', 'REQMORE', 'BYE', 'GREET', 'OFFERBOOK', 'OFFERBOOKED', 'ASK', 'DELIVERY_SUPPORT',
                        'SKILL_INTRODUCTION', 'SCHEDULE_RECOMMEND', 'THANK'])
  --slot SLOT           the list of dictionaries with slot_name key and slot_value value (or the text file) (default: [{'name': 'departure_date', 'description': 'The desired departure date for the flight', 'is_categorical': False}, {'name': 'departure_time_range', 'description': 'The desired departure time range for the
                        flight', 'is_categorical': False}, {'name': 'passenger_name', 'description': 'The name of the first passenger', 'is_categorical': False}, {'name': 'credit_card_number', 'description': 'The credit card number for payment', 'is_categorical': False}, {'name': 'expiry_date', 'description': 'The expiry
                        date of the credit card', 'is_categorical': False}])
  --intent INTENT       the list of dictionaries with intents information (intent_name, intent_description, intent_required_slots) (or the text file) (default: [{'name': 'search_flight', 'description': "Search for a flight based on user's preferences", 'slots': ['departure_date', 'departure_time_range']}, {'name':
                        'provide_date_and_time', 'description': 'Provide the desired departure date and time range for the flight', 'slots': ['departure_date', 'departure_time_range']}, {'name': 'provide_flight_details', 'description': 'Provide details of the found flight', 'slots': []}, {'name': 'provide_direct_flight',
                        'description': 'Provide information about the direct flight', 'slots': []}, {'name': 'provide_price_and_availability', 'description': 'Provide the price and availability details of the flight', 'slots': []}, {'name': 'provide_arrival_time', 'description': 'Provide the estimated arrival time at the
                        destination', 'slots': []}, {'name': 'book_tickets', 'description': 'Book tickets for the selected flight', 'slots': ['passenger_name_1', 'passenger_name_2']}, {'name': 'request_passenger_info', 'description': 'Request passenger information for booking', 'slots': []}, {'name':
                        'provide_passenger_info', 'description': 'Provide passenger information for booking', 'slots': ['passenger_name_1', 'passenger_name_2']}, {'name': 'confirm_booking', 'description': 'Confirm the booking of tickets', 'slots': []}, {'name': 'choose_payment_method', 'description': 'Choose a payment
                        method for the booking', 'slots': []}, {'name': 'request_credit_card_info', 'description': 'Request credit card information for payment', 'slots': []}, {'name': 'provide_credit_card_info', 'description': 'Provide credit card information for payment', 'slots': ['credit_card_number', 'expiry_date']},
                        {'name': 'confirm_payment', 'description': 'Confirm the successful payment and booking', 'slots': []}, {'name': 'ask_additional_assistance', 'description': 'Offer additional assistance to the user', 'slots': []}, {'name': 'ask_tourist_attractions', 'description': 'Inquire about tourist attractions at
                        the destination', 'slots': []}])
  --num_dialog NUM_DIALOG
                        the number of dialogs (default: 1)
  --list_product LIST_PRODUCT
  --save_path SAVE_PATH
                        the save path (.json) (default: dialog.json)
