from langchain_core.tools import tool
from typing import Dict, List, Tuple

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
      {
        "airline": "Vietnam Airlines",
        "departure": "06:00",
        "arrival": "07:20",
        "price": 1450000,
        "class": "economy"
      },
      {
        "airline": "Vietnam Airlines",
        "departure": "14:00",
        "arrival": "15:20",
        "price": 2800000,
        "class": "business"
      },
      {
        "airline": "VietJet Air",
        "departure": "08:30",
        "arrival": "09:50",
        "price": 890000,
        "class": "economy"
      },
      {
        "airline": "Bamboo Airways",
        "departure": "11:00",
        "arrival": "12:20",
        "price": 1200000,
        "class": "economy"
      }
    ],

    ("Hà Nội", "Phú Quốc"): [
      {
        "airline": "Vietnam Airlines",
        "departure": "07:00",
        "arrival": "09:15",
        "price": 2100000,
        "class": "economy"
      },
      {
        "airline": "VietJet Air",
        "departure": "10:00",
        "arrival": "12:15",
        "price": 1350000,
        "class": "economy"
      },
      {
        "airline": "VietJet Air",
        "departure": "16:00",
        "arrival": "18:15",
        "price": 1100000,
        "class": "economy"
      }
    ],

    ("Hà Nội", "Hồ Chí Minh"): [
      {
        "airline": "Vietnam Airlines",
        "departure": "06:00",
        "arrival": "08:10",
        "price": 1600000,
        "class": "economy"
      },
      {
        "airline": "VietJet Air",
        "departure": "07:30",
        "arrival": "09:40",
        "price": 950000,
        "class": "economy"
      },
      {
        "airline": "Bamboo Airways",
        "departure": "12:00",
        "arrival": "14:10",
        "price": 1300000,
        "class": "economy"
      },
      {
        "airline": "Vietnam Airlines",
        "departure": "18:00",
        "arrival": "20:10",
        "price": 3200000,
        "class": "business"
      }
    ],

    ("Hồ Chí Minh", "Đà Nẵng"): [
      {
        "airline": "Vietnam Airlines",
        "departure": "09:00",
        "arrival": "10:20",
        "price": 1300000,
        "class": "economy"
      },
      {
        "airline": "VietJet Air",
        "departure": "13:00",
        "arrival": "14:20",
        "price": 780000,
        "class": "economy"
      }
    ],

    ("Hồ Chí Minh", "Phú Quốc"): [
      {
        "airline": "Vietnam Airlines",
        "departure": "08:00",
        "arrival": "09:00",
        "price": 1100000,
        "class": "economy"
      },
      {
        "airline": "VietJet Air",
        "departure": "15:00",
        "arrival": "16:00",
        "price": 650000,
        "class": "economy"
      }
    ]
  }

HOTELS_DB = {
    "Đà Nẵng": [
      {
        "name": "Mường Thanh Luxury",
        "stars": 5,
        "price_per_night": 1800000,
        "area": "Mỹ Khê",
        "rating": 4.5
      },
      {
        "name": "Sala Danang Beach",
        "stars": 4,
        "price_per_night": 1200000,
        "area": "Mỹ Khê",
        "rating": 4.3
      },
      {
        "name": "Fivitel Danang",
        "stars": 3,
        "price_per_night": 650000,
        "area": "Sơn Trà",
        "rating": 4.1
      },
      {
        "name": "Memory Hostel",
        "stars": 2,
        "price_per_night": 250000,
        "area": "Hải Châu",
        "rating": 4.6
      },
      {
        "name": "Christina's Homestay",
        "stars": 2,
        "price_per_night": 350000,
        "area": "An Thượng",
        "rating": 4.7
      }
    ],

    "Phú Quốc": [
      {
        "name": "Vinpearl Resort",
        "stars": 5,
        "price_per_night": 3500000,
        "area": "Bãi Dài",
        "rating": 4.4
      },
      {
        "name": "Sol by Meliá",
        "stars": 4,
        "price_per_night": 1500000,
        "area": "Bãi Trường",
        "rating": 4.2
      },
      {
        "name": "Lahana Resort",
        "stars": 3,
        "price_per_night": 800000,
        "area": "Dương Đông",
        "rating": 4.0
      },
      {
        "name": "9Station Hostel",
        "stars": 2,
        "price_per_night": 200000,
        "area": "Dương Đông",
        "rating": 4.5
      }
    ],

    "Hồ Chí Minh": [
      {
        "name": "Rex Hotel",
        "stars": 5,
        "price_per_night": 2800000,
        "area": "Quận 1",
        "rating": 4.3
      },
      {
        "name": "Liberty Central",
        "stars": 4,
        "price_per_night": 1400000,
        "area": "Quận 1",
        "rating": 4.1
      },
      {
        "name": "Cochin Zen Hotel",
        "stars": 3,
        "price_per_night": 550000,
        "area": "Quận 3",
        "rating": 4.4
      },
      {
        "name": "The Common Room",
        "stars": 2,
        "price_per_night": 180000,
        "area": "Quận 1",
        "rating": 4.6
      }
    ]
  }

# some utility functions
def _format_price_vnd(price: int) -> str:
    return f"{price:,}".replace(",", ".") + " VNĐ"

def _normalize_city(city: str) -> str:
    return " ".join(city.strip().split())

def _format_flights(origin: str, destination: str, flights: List[dict]) -> str:
    flights = sorted(flights, key=lambda x: x["price"])
    lines = [f"Các chuyến bay từ {origin} đến {destination}:"]

    for i, flight in enumerate(flights, start=1):
        lines.append(
            f"{i}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
            f"{flight['class']} | {_format_price_vnd(flight['price'])}"
        )

    return "\n".join(lines)

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.

    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy chuyến bay trực tiếp, thử tra ngược chiều.
    Nếu vẫn không có, trả về thông báo không có chuyến.
    """
    origin = _normalize_city(origin)
    destination = _normalize_city(destination)

    if not origin or not destination:
        return "Vui lòng cung cấp đầy đủ thành phố khởi hành và thành phố đến."

    # 1. Tìm đúng chiều
    direct_flights = FLIGHTS_DB.get((origin, destination))
    if direct_flights:
        return _format_flights(origin, destination, direct_flights)
    
    # 2. Không có thì thử tra ngược chiều
    reverse_flights = FLIGHTS_DB.get((destination, origin))
    if reverse_flights:
        return (
            f"Không tìm thấy chuyến bay trực tiếp từ {origin} đến {destination}.\n"
            f"Tuy nhiên, có các chuyến bay chiều ngược lại từ {destination} đến {origin}:\n"
            + "\n".join(_format_flights(destination, origin, reverse_flights).split("\n")[1:])
        )
    
    # 3. Không có cả hai chiều
    return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."


@tool
def search_hotels(city: str, max_price_per_night: int=99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating
    """
    city = _normalize_city(city)
    
    if not city:
        return "Vui lòng cung cấp tên thành phố."
    
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."
    
    filtered_hotels = [
        hotel for hotel in hotels if hotel["price_per_night"] <= max_price_per_night
    ]

    if not filtered_hotels:
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới "
            f"{_format_price_vnd(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
        )
    
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)

    lines = [
        f"Các khách sạn tại {city} phù hợp với ngân sách dưới {_format_price_vnd(max_price_per_night)}/đêm:"
    ]

    for i, hotel in enumerate(filtered_hotels, start=1):
        lines.append(
            f"{i}. {hotel['name']} | {hotel['stars']} sao | "
            f"{_format_price_vnd(hotel['price_per_night'])}/đêm | "
            f"Khu vực: {hotel['area']} | Rating: {hotel['rating']}"
        )

    return "\n".join(lines)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')

    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    if total_budget < 0:
        return "Ngân sách ban đầu không hợp lệ."

    if not expenses or not expenses.strip():
        return (
            "Bảng chi phí:\n"
            "--------------------\n"
            f"Tổng chi: {_format_price_vnd(0)}\n"
            f"Ngân sách: {_format_price_vnd(total_budget)}\n"
            f"Còn lại: {_format_price_vnd(total_budget)}"
        )

    expense_dict = {}

    try:
        items = [item.strip() for item in expenses.split(",") if item.strip()]

        for item in items:
            if ":" not in item:
                return (
                    "Định dạng expenses không hợp lệ. "
                    "Vui lòng dùng dạng 'tên_khoản:số_tiền', các khoản cách nhau bởi dấu phẩy."
                )

            name, value = item.split(":", 1)
            name = name.strip()
            value = value.strip()

            if not name:
                return "Tên khoản chi không được để trống."

            amount = int(value)
            if amount < 0:
                return f"Khoản chi '{name}' không hợp lệ vì số tiền âm."

            expense_dict[name] = amount

    except ValueError:
        return (
            "Định dạng expenses không hợp lệ. "
            "Số tiền phải là số nguyên, ví dụ: 'vé_máy_bay:890000,khách_sạn:650000'."
        )

    total_expense = sum(expense_dict.values())
    remaining = total_budget - total_expense

    lines = ["Bảng chi phí:"]
    for name, amount in expense_dict.items():
        display_name = name.replace("_", " ").capitalize()
        lines.append(f"- {display_name}: {_format_price_vnd(amount)}")

    lines.append("--------------------")
    lines.append(f"Tổng chi: {_format_price_vnd(total_expense)}")
    lines.append(f"Ngân sách: {_format_price_vnd(total_budget)}")

    if remaining >= 0:
        lines.append(f"Còn lại: {_format_price_vnd(remaining)}")
    else:
        lines.append(f"Vượt ngân sách {_format_price_vnd(abs(remaining))}! Cần điều chỉnh.")

    return "\n".join(lines)