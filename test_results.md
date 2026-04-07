# KẾT QUẢ KIỂM THỬ AGENT TRAVELBUDDY

## Test 1: Direct Answer
**User:** `Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`

**Log hệ thống:**
```
Human: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
AI: Chào bạn! Bạn có ý tưởng nào về địa điểm mình muốn khám phá chưa? Hay mình có thể tư vấn cho bạn một số điểm đến thú vị ở Việt Nam? 
```

---

## Test 2: Single Tool Call
**User:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`

**Log hệ thống:**
```
Human: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
[AI gọi tool: search_flights]({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Tool: Các chuyến bay Hà Nội → Đà Nẵng:
1. VietJet Air | 08:30-09:50 | economy | 890.000đ
2. Bamboo Airways | 11:00-12:20 | economy | 1.200.000đ
3. Vietnam Airlines | 06:00-07:20 | economy | 1.450.000đ
4. Vietnam Airlines | 14:00-15:20 | business | 2.800.000đ
AI: Đây là thông tin các chuyến bay từ Hà Nội đi Đà Nẵng cho bạn:

1. **VietJet Air**: 08:30 - 09:50 | Phân hạng: Economy | Giá: 890.000 đ
2. **Bamboo Airways**: 11:00 - 12:20 | Phân hạng: Economy | Giá: 1.200.000 đ
3. **Vietnam Airlines**: 06:00 - 07:20 | Phân hạng: Economy | Giá: 1.450.000 đ
4. **Vietnam Airlines**: 14:00 - 15:20 | Phân hạng: Business | Giá: 2.800.000 đ

Nếu bạn cần thêm thông tin gì hoặc muốn đặt vé, đừng ngần ngại hỏi nhé!
```

---

## Test 3: Multi-step Tool Chaining
**User:** `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp.`

**Log hệ thống:**
```
Human: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp.
[AI gọi tool: search_flights]({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Tool: Các chuyến bay Hà Nội → Phú Quốc:
1. VietJet Air | 16:00-18:15 | economy | 1.100.000đ
2. VietJet Air | 10:00-12:15 | economy | 1.350.000đ
3. Vietnam Airlines | 07:00-09:15 | economy | 2.100.000đ
[AI gọi tool: calculate_budget]({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000'})
Tool: Bảng chi phí:
- vé máy bay: 1.100.000đ
---
Tổng chi: 1.100.000đ
Ngân sách: 5.000.000đ
Còn lại: 3.900.000đ
[AI gọi tool: search_hotels]({'city': 'Phú Quốc', 'max_price_per_night': 1950000})
Tool: Khách sạn tại Phú Quốc (<= 1.950.000đ/đêm):
1. 9Station Hostel | 2★ | Dương Đông | rating 4.5 | 200.000đ/đêm
2. Sol by Meliá | 4★ | Bãi Trường | rating 4.2 | 1.500.000đ/đêm
3. Lahana Resort | 3★ | Dương Đông | rating 4.0 | 800.000đ/đêm
[AI gọi tool: calculate_budget]({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:3000000'})
Tool: Bảng chi phí:
- vé máy bay: 1.100.000đ
- khách sạn: 3.000.000đ
---
Tổng chi: 4.100.000đ
Ngân sách: 5.000.000đ
Còn lại: 900.000đ
AI: ### Kế hoạch chuyến đi
**Chuyến bay:**  
- VietJet Air | 16:00-18:15 | Giá: 1.100.000đ

**Khách sạn:**  
- Sol by Meliá | 4★ | Bãi Trường | Giá: 1.500.000đ/đêm  
(Tổng cho 2 đêm: 3.000.000đ)

**Ngân sách:**  
- Tổng chi phí: 4.100.000đ  
- Tiền dư sau khi chi tiêu: 900.000đ  

**Gợi ý:**  
- Bạn có 900.000đ dư, có thể dùng để ăn uống, tham quan tại Phú Quốc. Nên thưởng thức hải sản tươi ngon ở chợ đêm Dinh Cậu hay trải nghiệm các hoạt động trên biển nhé!

Nếu cần thêm thông tin hay thay đổi gì, hãy cho mình biết nhé!
```

---

## Test 4: Missing Info / Clarification
**User:** `Tôi muốn đặt khách sạn`

**Log hệ thống:**
```
Human: Tôi muốn đặt khách sạn
AI: Bạn đang tìm khách sạn ở đâu? Và bạn có ngân sách cho mỗi đêm hay không?
```

---

## Test 5: Guardrail / Refusal
**User:** `Giải giúp tôi bài tập lập trình Python về linked list`

**Log hệ thống:**
```
Human: Giải giúp tôi bài tập lập trình Python về linked list
AI: Mình rất tiếc, nhưng mình không thể giúp bạn với bài tập lập trình. Tuy nhiên, nếu bạn có bất kỳ câu hỏi nào liên quan đến du lịch, vé máy bay hoặc khách sạn, hãy cho mình biết nhé!
```

---

