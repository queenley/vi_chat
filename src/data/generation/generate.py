import argparse
import json
from dialog_generation import DialogGenerate
    

def make_parser():
    parser = argparse.ArgumentParser("Vietnamese Dialog Generation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--key", 
                        type=str, 
                        required=True, 
                        help="the private key of ChatGPT API")
    parser.add_argument("--domain", 
                        type=str, 
                        default="Flight", 
                        help="the domain of dialog")
    parser.add_argument("--domain_type", 
                        type=str, 
                        default="booking", 
                        help="the domain type of dialog. (service, trading, ...)")
    # parser.add_argument("--product", 
    #                     type=str, 
    #                     default="haircut", 
    #                     help="the product of dialog")
    parser.add_argument("--example", 
                        help="the example dialog",
                        default=[
                                    "USER:  Xin chào, tôi chán quá",
                                    "SYSTEM: Xin chào, tôi sẵn sàng ở đây để trò chuyện cùng bạn.",
                                    "USER: Tôi muốn thực hiện chuyến du lịch từ Thành phố Hồ Chí Minh đến Đà Lạt. Tôi cần 2 vé một chiều vào thứ ba tuần sau. ",
                                    "SYSTEM: Có một chuyến bay khởi hành lúc 5:00 sáng, không có điểm dừng, với mức phí là 1.000.000 VNĐ cho 1 người. ",
                                    "USER:  Tôi sẽ đến Đà Lạt vào lúc mấy giờ? ",
                                    "SYSTEM: Khoảng 6:00 sáng bạn sẽ đến Đà Lạt. ",
                                    "USER: Tuyệt vời, chuyến bay này rất phù hợp với tôi. ",
                                    "SYSTEM: Bạn còn cần thêm yêu cầu gì nữa không? ",
                                    "USER: Đây là lần đầu tiên tôi đến Đà Lạt. Bạn có thể nói một chút về Đà Lạt cho tôi biết không? ",
                                    "SYSTEM: Đà Lạt là một thành phố thuộc tỉnh Lâm Đồng, nằm trên cao nguyên Lâm Viên, thuộc vùng Tây Nguyên, Việt Nam. Thành phố Đà Lạt có một khí hậu miền núi dịu mát ôn hòa quanh năm. USER: cảm ơn",
                                    "SYSTEM: không có chi, chúc bạn có chuyên đi vui vẻ"
                                ]
                        )
    parser.add_argument("--user_action", 
                        type=list, 
                        help="the list of user actions",
                        default=["INFORM", "REQUEST", "SELECT", "CONFIRM", "REQUEST-ALTS", "BYE", "GREET", "BOOK", "NOBOOK", "OFFERBOOK", "ASK", "INFORM-INTENT", "NEGATE-INTENT", "AFFIRM-INTENT", "AFFIRM", "NEGATE", "THANK"])
    parser.add_argument("--system_action", 
                        type=list, 
                        help="the list of system actions",
                        default=["INFORM", "REQUEST", "SELECT", "CONFIRM", "OFFER", "NoOFFER", "RECOMMEND", "PROMOTION_INTRODUCTION", "NOTIFY_SUCCESS", "NOTIFY_FALIURE", "INFORM_COUNT", "OFFER_INTENT", "REQMORE", "BYE", "GREET", "OFFERBOOK", "OFFERBOOKED", "ASK", "DELIVERY_SUPPORT", "SKILL_INTRODUCTION", "SCHEDULE_RECOMMEND", "THANK"])
    parser.add_argument("--slot", 
                        help="the list of dictionaries with slot_name key and slot_value value (or the text file)",
                        default=[
                                    {
                                        "name": "departure_date",
                                        "description": "The desired departure date for the flight",
                                        "is_categorical": False
                                    },
                                    {
                                        "name": "departure_time_range",
                                        "description": "The desired departure time range for the flight",
                                        "is_categorical": False
                                    },
                                    {
                                        "name": "passenger_name",
                                        "description": "The name of the first passenger",
                                        "is_categorical": False
                                    },                                    
                                    {
                                        "name": "credit_card_number",
                                        "description": "The credit card number for payment",
                                        "is_categorical": False
                                    },
                                    {
                                        "name": "expiry_date",
                                        "description": "The expiry date of the credit card",
                                        "is_categorical": False
                                    }
                                ]
)
    parser.add_argument("--intent", 
                        help="the list of dictionaries with intents information (intent_name, intent_description, intent_required_slots) (or the text file)",
                        default=[                                                            
                                    {
                                        "name": "search_flight",
                                        "description": "Search for a flight based on user's preferences",
                                        "slots": ["departure_date", "departure_time_range"]
                                    },
                                    {
                                        "name": "provide_date_and_time",
                                        "description": "Provide the desired departure date and time range for the flight",
                                        "slots": ["departure_date", "departure_time_range"]
                                    },
                                    {
                                        "name": "provide_flight_details",
                                        "description": "Provide details of the found flight",
                                        "slots": []
                                    },
                                    {
                                        "name": "provide_direct_flight",
                                        "description": "Provide information about the direct flight",
                                        "slots": []
                                    },
                                    {
                                        "name": "provide_price_and_availability",
                                        "description": "Provide the price and availability details of the flight",
                                        "slots": []
                                    },
                                    {
                                        "name": "provide_arrival_time",
                                        "description": "Provide the estimated arrival time at the destination",
                                        "slots": []
                                    },
                                    {
                                        "name": "book_tickets",
                                        "description": "Book tickets for the selected flight",
                                        "slots": ["passenger_name_1", "passenger_name_2"]
                                    },
                                    {
                                        "name": "request_passenger_info",
                                        "description": "Request passenger information for booking",
                                        "slots": []
                                    },
                                    {
                                        "name": "provide_passenger_info",
                                        "description": "Provide passenger information for booking",
                                        "slots": ["passenger_name_1", "passenger_name_2"]
                                    },
                                    {
                                        "name": "confirm_booking",
                                        "description": "Confirm the booking of tickets",
                                        "slots": []
                                    },
                                    {
                                        "name": "choose_payment_method",
                                        "description": "Choose a payment method for the booking",
                                        "slots": []
                                    },
                                    {
                                        "name": "request_credit_card_info",
                                        "description": "Request credit card information for payment",
                                        "slots": []
                                    },
                                    {
                                        "name": "provide_credit_card_info",
                                        "description": "Provide credit card information for payment",
                                        "slots": ["credit_card_number", "expiry_date"]
                                    },
                                    {
                                        "name": "confirm_payment",
                                        "description": "Confirm the successful payment and booking",
                                        "slots": []
                                    },
                                    {
                                        "name": "ask_additional_assistance",
                                        "description": "Offer additional assistance to the user",
                                        "slots": []
                                    },
                                    {
                                        "name": "ask_tourist_attractions",
                                        "description": "Inquire about tourist attractions at the destination",
                                        "slots": []
                                    }
                                ]
                        )

    parser.add_argument("--num_dialog", 
                        type=int, 
                        help="the number of dialogs",            
                        default=1)
    parser.add_argument("--list_product", 
                        type=list, 
                        default=[])
    
    parser.add_argument("--save_path", 
                        type=str, 
                        help="the save path (.json)", 
                        default="dialog.json")

    return parser


if __name__=="__main__":
    args = make_parser().parse_args()        
     
    args_slot = args.slot
    args_intent = args.intent

    # Check slot information are a list or a text
    if isinstance(args_slot, str):
        try:
            with open(args_slot) as f:
                slots = f.readlines()
        except:
            print("Be sure the text file correctly")
    else:
         slots = args_slot

    # Check intent information are a list or a text
    if isinstance(args_intent, str):
        try:
            with open(args_intent) as f:
                intents = f.readlines()
        except:
            print("Be sure the text file correctly")
    else:
         intents = args_intent         
             
    # Call DialogGenerate object
    dialog_generation = DialogGenerate(
                        args.key,
                        args.domain,
                        args.domain_type,
                        # args.product, 
                        args.example,
                        args.user_action,
                        args.system_action,
                        slots,
                        intents,
                        args.list_product
                    )
        
    # Generate multiple dialog
    if args.num_dialog == len(args.list_product): 
        generated_dialog = dialog_generation.generate_multi_dialog()                   
    # Generate one dialog
    else:     
        generated_dialog = dialog_generation.generate_one_dialog()    

    with open(args.save_path, "w",  encoding ='utf8') as f:
            json.dump(generated_dialog, f, ensure_ascii = False)

    print(f"\nThe final dialog is saved to {args.save_path}")
