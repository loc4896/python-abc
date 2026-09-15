import os
import mysql.connector

class KetNoiDatabase:

    @staticmethod
    def ketnoi():
        return mysql.connector.connect(
            host=os.environ.get("MYSQLHOST"),
            port=int(os.environ.get("MYSQLPORT", 3306)),
            user=os.environ.get("MYSQLUSER"),
            password=os.environ.get("MYSQLPASSWORD"),
            database=os.environ.get("MYSQLDATABASE")
        )

class DoiTuong:
    def __init__(self,ma,ten):
        self.ma=ma
        self.ten=ten

    def nhap(self):
        self.ma=input("Nhập mã: ")
        self.ten=input("Nhập tên: ")

    def xuat(self):
        print("Mã:",self.ma)
        print("Tên:",self.ten)

#class con, class đơn hàng
class DonHang(DoiTuong):
           def __init__(self,ma="",ten="",makhachhang="",masanpham="",soluong=0,dathanhtoan=0):
                super().__init__(ma,ten)
                self.makhachhang=makhachhang
                self.masanpham=masanpham
                self.soluong=soluong
                self.dathanhtoan=dathanhtoan
                
           def nhap(self):
                super().nhap()
                self.makhachhang=input("Nhập mã khách hàng: ")
                self.masanpham=input("Nhập mã sản phẩm: ")
                self.soluong=int(input("Nhập số lượng: "))
                self.dathanhtoan=float(input("Nhập số tiền đã thanh toán: "))
                
           def xuat(self):
                super().xuat()
                print("Mã khách hàng:",self.makhachhang)
                print("Mã sản phẩm:",self.masanpham)
                print("Số lượng:",self.soluong)
                print("Đã thanh toán:",self.dathanhtoan)
                

#class con, class khách hàng
class KhachHang(DoiTuong):
                    def __init__(self,ma="",ten="",khuvuc="",namsinh=0):
                        super().__init__(ma,ten)
                        self.khuvuc=khuvuc
                        self.namsinh=namsinh
                    def nhap(self):
                        super().nhap()
                        self.khuvuc=input("Nhập khu vực: ")
                        self.namsinh=int(input("Nhập năm sinh: "))
                    def xuat(self):
                        super().xuat()
                        print("khu vực:",self.khuvuc)
                        print("Năm sinh:",self.namsinh)
                        
#class con, clas sản phẩm
class SanPham(DoiTuong):
            def __init__(self,ma="",ten="",nhomhang="",gianhap=0,giaban=0,tonkho=0):
                 super().__init__(ma,ten)
                 self.nhomhang=nhomhang
                 self.gianhap=gianhap
                 self.giaban=giaban
                 self.tonkho=tonkho
            def nhap(self):
                super().nhap()
                self.nhomhang=input("Nhập nhóm hàng: ")
                self.gianhap=float(input("Nhập giá nhập: "))
                self.giaban=float(input("Nhập giá bán: "))
                self.tonkho=int(input("Nhập số lượng tồn kho: "))
            def loinhuanmotsp(self):
                return self.giaban-self.gianhap
            def xuat(self):
                super().xuat()
                print("Nhóm hang:",self.nhomhang)
                print("Giá nhập:",self.gianhap)
                print("Giá bán:",self.giaban)
                print("Tồn kho:",self.tonkho)
                print("Lợi nhuận/sp:",self.loinhuanmotsp())

class QuanLyABC:

    def __init__(self):
        self.dskhachhang = []
        self.dssanpham = []
        self.dsdonhang = []

        self.conn = KetNoiDatabase.ketnoi()

        self.doc_khachhang_mysql()
        self.doc_sanpham_mysql()
        self.doc_donhang_mysql()
        
    def themkhachhang(self):

        print("\n========= THÊM KHÁCH HÀNG =========")

        kh = KhachHang()
        kh.nhap()

        sql = """
            INSERT INTO khachhang
            (ma, ten, khuvuc, namsinh)
            VALUES (%s, %s, %s, %s)
        """

        cursor = self.conn.cursor()

        try:

            cursor.execute(sql, (
            kh.ma,
            kh.ten,
            kh.khuvuc,
            kh.namsinh
            ))

            self.conn.commit()

            self.dskhachhang.append(kh)

            print("Đã thêm khách hàng vào MySQL!")

        except mysql.connector.Error as e:

               print("Lỗi:", e)

        finally:

               cursor.close()

    def hienthikhachhang(self):
                print("\n==========DANH SÁCH KHÁCH HÀNG============")
                if len(self.dskhachhang)==0:
                    print("Danh sách rỗng!")
                    return
                for kh in self.dskhachhang:
                    print("------------------------")
                    kh.xuat()
                    
    def timkhachhang(self):
                ma=input("Nhập mã khách hàng cần tìm: ")
                for kh in self.dskhachhang:
                    if kh.ma==ma:
                        print("\n Tìm thấy khách hàng:")
                        kh.xuat()
                        return
                print("Không tìm thấy khách hàng!")
                

    def themsanpham(self):

        print("\n============ THÊM SẢN PHẨM ============")

        sp = SanPham()
        sp.nhap()

        sql = """
             INSERT INTO sanpham
             (ma, ten, nhomhang, gianhap, giaban, tonkho)
             VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor = self.conn.cursor()

        try:

            cursor.execute(sql, (
                  sp.ma,
                  sp.ten,
                  sp.nhomhang,
                  sp.gianhap,
                  sp.giaban,
                  sp.tonkho
            ))

            self.conn.commit()

            self.dssanpham.append(sp)

            print("Đã thêm sản phẩm vào MySQL!")

        except mysql.connector.Error as e:

              print("Lỗi:", e)

        finally:

              cursor.close()
              
    def hienthisanpham(self):
                print("\n==========DANH SÁCH SẢN PHẨM===========")
                if len(self.dssanpham)==0:
                    print("Danh sách rỗng!")
                    return
                for sp in self.dssanpham:
                    print("-------------------")
                    sp.xuat()
                    
    def timsanpham(self):
                ma=input("Nhập mã sản phẩm cần tìm: ")
                for sp in self.dssanpham:
                    if sp.ma==ma:
                        print("\n Tìm thấy sản phẩm:")
                        sp.xuat()
                        return
                print("Không tìm thấy sản phẩm!")

    def themdonhang(self):

         print("\n======== THÊM ĐƠN HÀNG =========")

         dh = DonHang()
         dh.nhap()

         sql = """
               INSERT INTO donhang
               (ma, ten, makhachhang, masanpham, soluong, dathanhtoan)
               VALUES (%s, %s, %s, %s, %s, %s)
         """

         cursor = self.conn.cursor()

         try:

            cursor.execute(sql, (
            dh.ma,
            dh.ten,
            dh.makhachhang,
            dh.masanpham,
            dh.soluong,
            dh.dathanhtoan
            ))

            self.conn.commit()

            self.dsdonhang.append(dh)

            print("Đã thêm đơn hàng vào MySQL!")

         except mysql.connector.Error as e:

               print("Lỗi:", e)

         finally:

               cursor.close()
    def hienthidonhang(self):
                print("\n===========DANH SÁCH ĐƠN HÀNG===========")
                if len(self.dsdonhang)==0:
                    print("Danh sách rỗng!")
                    return
                for dh in self.dsdonhang:
                    print("----------------------")
                    dh.xuat()
                    
            #class quản lý, tìm sản phẩm theo mã
    def laysanpham(self,masanpham):
                for sp in self.dssanpham:
                    if sp.ma==masanpham:
                        return sp
                return None
            
            #class quản lý, tính doanh thu đơn hàng
    def tinhdoanhthudonhang(self,dh):
                sp=self.laysanpham(dh.masanpham)
                if sp is None:
                    return 0
                return dh.soluong*sp.giaban
            
            #class quản lý, tính lợi nhuận đơn hàng
    def tinhloinhuandonhang(self,dh):
                sp=self.laysanpham(dh.masanpham)
                if sp is None:
                    return 0
                doanhthu=(dh.soluong*sp.giaban)
                giavon=(dh.soluong*sp.gianhap)
                return doanhthu-giavon
            
            #class quản lý, hiển thị doanh thu từng đơn hàng
    def hienthidoanhthu(self):
                print("\n===========DOANH THU TỪNG ĐƠN HÀNG=============")
                if len(self.dsdonhang)==0:
                    print("Chưa có đơn hàng!")
                    return
                for dh in self.dsdonhang:
                    doanhthu=(self.tinhdoanhthudonhang(dh))
                    print(dh.ma,"-",dh.masanpham,"-",dh.soluong,"SP -",doanhthu,"VNĐ")
                    
            #class quản lý, tổng doanh thu
    def tongdoanhthu(self):
                tong=0
                for dh in self.dsdonhang:
                    tong+=(self.tinhdoanhthudonhang(dh))
                return tong
            
    def hienthitongdoanhthu(self):
                tong=self.tongdoanhthu()
                print("\n===========TỔNG DOANH THU===========")
                print(tong,"VNĐ")
                
            #class quản lý, tổng lợi nhuận
    def tongloinhuan(self):
                tong=0
                for dh in self.dsdonhang:
                    tong+=(self.tinhloinhuandonhang(dh))
                return tong
            
    def hienthitongloinhuan(self):
                tong=self.tongloinhuan()
                print("\n============TỔNG LỢI NHUẬN============")
                print(tong,"VNĐ")
                
            #class quản lý, tổng doanh thu theo sản phẩm
    def doanhthutheosanpham(self):
                print("\n==========DOANH THU THEO SẢN PHẨM===========")
                if len(self.dsdonhang)==0:
                    print("Chưa có đơn hàng!")
                    return
                ketqua={}
                for dh in self.dsdonhang:
                    doanhthu=(self.tinhdoanhthudonhang(dh))
                    masp=dh.masanpham
                    if masp in ketqua:
                        ketqua[masp]+=doanhthu
                    else:
                        ketqua[masp]=doanhthu
                for masp,doanhthu in ketqua.items():
                    sp=self.laysanpham(masp)
                    if sp is not None:
                        print(sp.ten,":",doanhthu,"VNĐ")
                        
            #class quản lý, tìm sản phẩm doanh thu cao nhất
    def sanphamdoanhthucaonhat(self):
                if len(self.dsdonhang)==0:
                    print("Chưa có dữ liệu!")
                    return
                ketqua={}
                for dh in self.dsdonhang:
                    doanhthu=(self.tinhdoanhthudonhang(dh))
                    masp=dh.masanpham
                    if masp in ketqua:
                        ketqua[masp]+=doanhthu
                    else:
                        ketqua[masp]=doanhthu
                mamax=max(ketqua,key=ketqua.get)
                sp=self.laysanpham(mamax)
                print("\n==========SẢN PHẨM DOANH THU CAO NHẤT==============")
                print("Sản phẩm:",sp.ten)
                print("Doanh thu:",ketqua[mamax],"VNĐ")
                
            #class quản lý, thống kê toàn bộ
    def thongke(self):
                print("\n=============================")
                print("    THỐNG KÊ CÔNG TY ABC")
                print("==============================")
                print("Số khách hàng:",len(self.dskhachhang))
                print("Số sản phẩm:",len(self.dssanpham))
                print("Số đơn hàng:",len(self.dsdonhang))
                print("Tổng doanh thu:",self.tongdoanhthu(),"VNĐ")
                print("Tổng lợi nhuận:",self.tongloinhuan(),"VNĐ")

    def doc_khachhang_mysql(self):

         self.dskhachhang = []

         cursor = self.conn.cursor()

         sql = """
              SELECT ma, ten, khuvuc, namsinh
              FROM khachhang
         """

         cursor.execute(sql)

         rows = cursor.fetchall()

         for row in rows:

             kh = KhachHang(
                row[0],
                row[1],
                row[2],
                row[3]
             )

             self.dskhachhang.append(kh)

         cursor.close()

    def doc_sanpham_mysql(self):

         self.dssanpham = []

         cursor = self.conn.cursor()

         sql = """
              SELECT ma, ten, nhomhang, gianhap, giaban, tonkho
              FROM sanpham
         """

         cursor.execute(sql)

         rows = cursor.fetchall()

         for row in rows:

             sp = SanPham(
                 row[0],
                 row[1],
                 row[2],
                 row[3],
                 row[4],
                 row[5]
             )

             self.dssanpham.append(sp)

         cursor.close()

    def doc_donhang_mysql(self):

         self.dsdonhang = []

         cursor = self.conn.cursor()

         sql = """
               SELECT ma, ten, makhachhang,
                    masanpham, soluong, dathanhtoan
               FROM donhang
         """

         cursor.execute(sql)

         rows = cursor.fetchall()

         for row in rows:

             dh = DonHang(
                 row[0],
                 row[1],
                 row[2],
                 row[3],
                 row[4],
                 row[5]
             )

             self.dsdonhang.append(dh)

         cursor.close()
         
     #tính tổng công nợ
    def tinhcongno(self,dh):
                doanhthu=self.tinhdoanhthudonhang(dh)
                congno=doanhthu-dh.dathanhtoan
                return congno
            
    def tongcongno(self):
                tong=0

                for dh in self.dsdonhang:
                    tong+=self.tinhcongno(dh)

                return tong

    def hienthitongcongno(self):
                print("\n========== TỔNG CÔNG NỢ ==========")
                print(self.tongcongno(),"VNĐ")

            #tính công nợ riêng từng khách hàng
    def tinhcongnokh(self):
                makh = input("Nhập mã khách hàng cần tính công nợ: ")

                tongcongno = 0
                co_don = False

                print("\n========== CÔNG NỢ KHÁCH HÀNG ==========")
                print("Mã khách hàng:", makh)

                for dh in self.dsdonhang:
                    # Kiểm tra đơn hàng có thuộc khách hàng này không
                    if dh.makhachhang == makh:
                       co_don = True
                    # Tìm sản phẩm của đơn hàng
                       sp = self.laysanpham(dh.masanpham)
                       if sp is None:
                          print("Không tìm thấy sản phẩm:", dh.masanpham)
                          continue
                       # Tính thành tiền
                       thanhtien = dh.soluong * sp.giaban
                       # Tính công nợ của đơn này
                       congno = thanhtien - dh.dathanhtoan
                       # Cộng vào tổng công nợ
                       tongcongno += congno
                       print("----------------------------------------")
                       print("Mã đơn hàng:", dh.ma)
                       print("Mã sản phẩm:", dh.masanpham)
                       print("Tên sản phẩm:", sp.ten)
                       print("Số lượng:", dh.soluong)
                       print("Thành tiền:", thanhtien, "VNĐ")
                       print("Đã thanh toán:", dh.dathanhtoan, "VNĐ")
                       print("Công nợ đơn này:", congno, "VNĐ")
                if co_don == False:
                  print("Khách hàng này chưa có đơn hàng!")
                  return

                print("----------------------------------------")
                print("TỔNG CÔNG NỢ CỦA KHÁCH HÀNG NÀY:", tongcongno, "VNĐ")

            # Tìm những sản phẩm có cùng giá bán
    def sanphamcunggiaban(self):
              ketqua = {}
              for sp in self.dssanpham:
                  if sp.giaban in ketqua:
                     ketqua[sp.giaban].append(sp)
                  else:
                     ketqua[sp.giaban] = [sp]
              print("\n========== SẢN PHẨM CÓ CÙNG GIÁ BÁN ==========")
              co_san_pham = False
              for giaban, danhsach in ketqua.items():
                  # Chỉ lấy giá bán có từ 2 sản phẩm trở lên
                  if len(danhsach) >= 2:
                      co_san_pham = True                      
                      print("Giá bán:", giaban, "VNĐ")
                      for sp in danhsach:
                          print("Mã sản phẩm:", sp.ma)
                          print("Tên sản phẩm:", sp.ten)
              if co_san_pham == False:
                 print("Không có sản phẩm nào cùng giá bán!")

            # Tìm khách hàng theo năm sinh
    def timkhachhangtheonamsinh(self):
                 namsinh=int(input("Nhập năm sinh cần tìm: "))
                 co_khach_hang=False
                 print("\n========== KHÁCH HÀNG THEO NĂM SINH ==========")
                 for kh in self.dskhachhang:
                     if kh.namsinh == namsinh:
                        co_khach_hang=True
                        print("--------------------------------")
                        kh.xuat()
                 if co_khach_hang == False:
                    print("Không tìm thấy khách hàng nào!")
      

#class menu
class Menu:

    def __init__(self):
        self.quanly = QuanLyABC()

    # MENU CHÍNH
    def hienthimenu(self):

        while True:

            print("\n")
            print("==========================================")
            print("        QUẢN LÝ DỮ LIỆU CÔNG TY ABC")
            print("==========================================")
            print("0. Thoát")
            print("1. Thêm khách hàng")
            print("2. Hiển thị khách hàng")
            print("3. Tìm khách hàng theo mã")
            print("4. Thêm sản phẩm")
            print("5. Hiển thị sản phẩm")
            print("6. Tìm sản phẩm")
            print("7. Thêm đơn hàng")
            print("8. Hiển thị đơn hàng")
            print("9. Tính doanh thu")
            print("10. Doanh thu theo sản phẩm")
            print("11. Sản phẩm doanh thu cao nhất")
            print("12. Thống kê")
            print("13. Tổng công nợ")
            print("14. Công nợ của từng khách hàng")
            print("15. Sản phẩm đồng giá")
            print("16. Tìm khách hàng theo năm sinh")
            print("==========================================")

            luachon = input("Nhập lựa chọn: ")

            
            if luachon == "0":
                print("Chương trình kết thúc!")
                break
            
            
            if luachon == "1":
                self.quanly.themkhachhang()

            elif luachon == "2":
                self.quanly.hienthikhachhang()

            elif luachon == "3":
                self.quanly.timkhachhang()
            
            elif luachon == "4":
                self.quanly.themsanpham()

            elif luachon == "5":
                self.quanly.hienthisanpham()

            elif luachon == "6":
                self.quanly.timsanpham()

            
            elif luachon == "7":
                self.quanly.themdonhang()

            elif luachon == "8":
                self.quanly.hienthidonhang()

            
            elif luachon == "9":
                self.quanly.hienthidoanhthu()
                self.quanly.hienthitongdoanhthu()
                self.quanly.hienthitongloinhuan()

            elif luachon == "10":
                self.quanly.doanhthutheosanpham()

            elif luachon == "11":
                self.quanly.sanphamdoanhthucaonhat()
            
            elif luachon == "12":
                self.quanly.thongke()
                
            elif luachon == "13":
                self.quanly.hienthitongcongno()
                
            elif luachon == "14":
                self.quanly.tinhcongnokh()
                
            elif luachon == "15":
                self.quanly.sanphamcunggiaban()
                
            elif luachon == "16":
                self.quanly.timkhachhangtheonamsinh()
            
            #nếu thêm mục nào thì viết tiếp dưới nhưng trên else dưới cùng

            else:
                print("Không tìm thấy mục này!")#nếu vượt qua số mục menu quy định sẽ hiện thông báo này

# ==========================================================
# PHẦN WEB LOCALHOST - GIỮ NGUYÊN CÁC CLASS OOP PHÍA TRÊN
# ==========================================================

from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Dùng đúng class quản lý hiện tại của bài
quanly = QuanLyABC()


# ----------------------------------------------------------
# Giao diện HTML chung
# ----------------------------------------------------------
def khung_trang(tieu_de, noi_dung):
    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>{tieu_de}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 1100px;
                margin: auto;
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 0 10px #ccc;
            }}
            h1, h2 {{
                text-align: center;
            }}
            .menu {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin-top: 20px;
            }}
            .menu a {{
                display: block;
                padding: 14px;
                background: #eeeeee;
                text-decoration: none;
                color: black;
                border-radius: 6px;
            }}
            .menu a:hover {{
                background: #dddddd;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            th, td {{
                border: 1px solid #999;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background: #eeeeee;
            }}
            input {{
                width: 97%;
                padding: 8px;
                margin: 5px 0 12px;
            }}
            button {{
                padding: 10px 18px;
                cursor: pointer;
            }}
            .box {{
                padding: 15px;
                margin: 12px 0;
                border: 1px solid #ccc;
                border-radius: 6px;
            }}
            .back {{
                display: inline-block;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {noi_dung}
        </div>
    </body>
    </html>
    """


@app.route("/")
def trangchu():
    noi_dung = """
    <h1>QUẢN LÝ DỮ LIỆU CÔNG TY ABC</h1>
    <p style="text-align:center;">Dữ Liệu Python + MySQL(load lên database) + Flask(chạy trên trình duyệt)</p>

    <div class="menu">
        <a href="/khachhang/them">1. Thêm khách hàng</a>
        <a href="/khachhang">2. Hiển thị khách hàng</a>
        <a href="/khachhang/tim">3. Tìm khách hàng theo mã</a>

        <a href="/sanpham/them">4. Thêm sản phẩm</a>
        <a href="/sanpham">5. Hiển thị sản phẩm</a>
        <a href="/sanpham/tim">6. Tìm sản phẩm</a>

        <a href="/donhang/them">7. Thêm đơn hàng</a>
        <a href="/donhang">8. Hiển thị đơn hàng</a>

        <a href="/doanhthu">9. Tính doanh thu</a>
        <a href="/doanhthu/sanpham">10. Doanh thu theo sản phẩm</a>
        <a href="/doanhthu/caonhat">11. Sản phẩm doanh thu cao nhất</a>
        <a href="/thongke">12. Thống kê</a>

        <a href="/congno">13. Tổng công nợ</a>
        <a href="/congno/khachhang">14. Công nợ của từng khách hàng</a>

        <a href="/sanpham/dongia">15. Sản phẩm đồng giá</a>
        <a href="/khachhang/namsinh">16. Tìm khách hàng theo năm sinh</a>
    </div>
    """
    return khung_trang("Quản lý ABC", noi_dung)


# ----------------------------------------------------------
# KHÁCH HÀNG
# ----------------------------------------------------------
@app.route("/khachhang")
def hienthi_khachhang():
    rows = ""
    for kh in quanly.dskhachhang:
        rows += f"""
        <tr>
            <td>{kh.ma}</td>
            <td>{kh.ten}</td>
            <td>{kh.khuvuc}</td>
            <td>{kh.namsinh}</td>
        </tr>
        """

    noi_dung = """
    <h2>DANH SÁCH KHÁCH HÀNG</h2>
    <table>
        <tr><th>Mã</th><th>Tên</th><th>Khu vực</th><th>Năm sinh</th></tr>
    """ + rows + """
    </table>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Khách hàng", noi_dung)


@app.route("/khachhang/them", methods=["GET", "POST"])
def them_khachhang():
    if request.method == "POST":
        ma = request.form["ma"]
        ten = request.form["ten"]
        khuvuc = request.form["khuvuc"]
        namsinh = int(request.form["namsinh"])

        kh = KhachHang(ma, ten, khuvuc, namsinh)

        sql = """
            INSERT INTO khachhang (ma, ten, khuvuc, namsinh)
            VALUES (%s, %s, %s, %s)
        """
        cursor = quanly.conn.cursor()
        try:
            cursor.execute(sql, (kh.ma, kh.ten, kh.khuvuc, kh.namsinh))
            quanly.conn.commit()
            quanly.dskhachhang.append(kh)
        finally:
            cursor.close()

        return redirect(url_for("hienthi_khachhang"))

    noi_dung = """
    <h2>THÊM KHÁCH HÀNG</h2>
    <form method="post">
        Mã:<br><input name="ma" required>
        Tên:<br><input name="ten" required>
        Khu vực:<br><input name="khuvuc" required>
        Năm sinh:<br><input name="namsinh" type="number" required>
        <button type="submit">Thêm khách hàng</button>
    </form>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Thêm khách hàng", noi_dung)


@app.route("/khachhang/tim", methods=["GET", "POST"])
def tim_khachhang_web():
    ketqua = ""
    if request.method == "POST":
        ma = request.form["ma"]
        for kh in quanly.dskhachhang:
            if kh.ma == ma:
                ketqua = f"""
                <div class="box">
                    <b>Mã:</b> {kh.ma}<br>
                    <b>Tên:</b> {kh.ten}<br>
                    <b>Khu vực:</b> {kh.khuvuc}<br>
                    <b>Năm sinh:</b> {kh.namsinh}
                </div>
                """
                break
        if ketqua == "":
            ketqua = "<p>Không tìm thấy khách hàng!</p>"

    noi_dung = f"""
    <h2>TÌM KHÁCH HÀNG THEO MÃ</h2>
    <form method="post">
        Mã khách hàng:<br><input name="ma" required>
        <button type="submit">Tìm</button>
    </form>
    {ketqua}
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Tìm khách hàng", noi_dung)


@app.route("/khachhang/namsinh", methods=["GET", "POST"])
def tim_khachhang_namsinh():
    ketqua = ""
    if request.method == "POST":
        namsinh = int(request.form["namsinh"])
        for kh in quanly.dskhachhang:
            if kh.namsinh == namsinh:
                ketqua += f"""
                <tr>
                    <td>{kh.ma}</td>
                    <td>{kh.ten}</td>
                    <td>{kh.khuvuc}</td>
                    <td>{kh.namsinh}</td>
                </tr>
                """
        if ketqua == "":
            ketqua = '<tr><td colspan="4">Không tìm thấy khách hàng nào!</td></tr>'

    noi_dung = f"""
    <h2>TÌM KHÁCH HÀNG THEO NĂM SINH</h2>
    <form method="post">
        Năm sinh:<br><input name="namsinh" type="number" required>
        <button type="submit">Tìm</button>
    </form>
    <table>
        <tr><th>Mã</th><th>Tên</th><th>Khu vực</th><th>Năm sinh</th></tr>
        {ketqua}
    </table>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Khách hàng theo năm sinh", noi_dung)


# ----------------------------------------------------------
# SẢN PHẨM
# ----------------------------------------------------------
@app.route("/sanpham")
def hienthi_sanpham():
    rows = ""
    for sp in quanly.dssanpham:
        rows += f"""
        <tr>
            <td>{sp.ma}</td>
            <td>{sp.ten}</td>
            <td>{sp.nhomhang}</td>
            <td>{sp.gianhap}</td>
            <td>{sp.giaban}</td>
            <td>{sp.tonkho}</td>
            <td>{sp.loinhuanmotsp()}</td>
        </tr>
        """

    noi_dung = """
    <h2>DANH SÁCH SẢN PHẨM</h2>
    <table>
        <tr>
            <th>Mã</th><th>Tên</th><th>Nhóm hàng</th>
            <th>Giá nhập</th><th>Giá bán</th>
            <th>Tồn kho</th><th>Lợi nhuận/SP</th>
        </tr>
    """ + rows + """
    </table>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Sản phẩm", noi_dung)


@app.route("/sanpham/them", methods=["GET", "POST"])
def them_sanpham():
    if request.method == "POST":
        ma = request.form["ma"]
        ten = request.form["ten"]
        nhomhang = request.form["nhomhang"]
        gianhap = float(request.form["gianhap"])
        giaban = float(request.form["giaban"])
        tonkho = int(request.form["tonkho"])

        sp = SanPham(ma, ten, nhomhang, gianhap, giaban, tonkho)

        sql = """
            INSERT INTO sanpham
            (ma, ten, nhomhang, gianhap, giaban, tonkho)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = quanly.conn.cursor()
        try:
            cursor.execute(sql, (
                sp.ma, sp.ten, sp.nhomhang,
                sp.gianhap, sp.giaban, sp.tonkho
            ))
            quanly.conn.commit()
            quanly.dssanpham.append(sp)
        finally:
            cursor.close()

        return redirect(url_for("hienthi_sanpham"))

    noi_dung = """
    <h2>THÊM SẢN PHẨM</h2>
    <form method="post">
        Mã:<br><input name="ma" required>
        Tên:<br><input name="ten" required>
        Nhóm hàng:<br><input name="nhomhang" required>
        Giá nhập:<br><input name="gianhap" type="number" step="any" required>
        Giá bán:<br><input name="giaban" type="number" step="any" required>
        Tồn kho:<br><input name="tonkho" type="number" required>
        <button type="submit">Thêm sản phẩm</button>
    </form>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Thêm sản phẩm", noi_dung)


@app.route("/sanpham/tim", methods=["GET", "POST"])
def tim_sanpham_web():
    ketqua = ""
    if request.method == "POST":
        ma = request.form["ma"]
        for sp in quanly.dssanpham:
            if sp.ma == ma:
                ketqua = f"""
                <div class="box">
                    <b>Mã:</b> {sp.ma}<br>
                    <b>Tên:</b> {sp.ten}<br>
                    <b>Nhóm hàng:</b> {sp.nhomhang}<br>
                    <b>Giá nhập:</b> {sp.gianhap}<br>
                    <b>Giá bán:</b> {sp.giaban}<br>
                    <b>Tồn kho:</b> {sp.tonkho}<br>
                    <b>Lợi nhuận/SP:</b> {sp.loinhuanmotsp()}
                </div>
                """
                break
        if ketqua == "":
            ketqua = "<p>Không tìm thấy sản phẩm!</p>"

    noi_dung = f"""
    <h2>TÌM SẢN PHẨM THEO MÃ</h2>
    <form method="post">
        Mã sản phẩm:<br><input name="ma" required>
        <button type="submit">Tìm</button>
    </form>
    {ketqua}
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Tìm sản phẩm", noi_dung)


@app.route("/sanpham/dongia")
def sanpham_dongia_web():
    ketqua = {}
    for sp in quanly.dssanpham:
        if sp.giaban in ketqua:
            ketqua[sp.giaban].append(sp)
        else:
            ketqua[sp.giaban] = [sp]

    rows = ""
    for giaban, danhsach in ketqua.items():
        if len(danhsach) >= 2:
            for sp in danhsach:
                rows += f"""
                <tr>
                    <td>{giaban}</td>
                    <td>{sp.ma}</td>
                    <td>{sp.ten}</td>
                </tr>
                """

    if rows == "":
        rows = '<tr><td colspan="3">Không có sản phẩm nào cùng giá bán!</td></tr>'

    noi_dung = f"""
    <h2>SẢN PHẨM CÓ CÙNG GIÁ BÁN</h2>
    <table>
        <tr><th>Giá bán</th><th>Mã sản phẩm</th><th>Tên sản phẩm</th></tr>
        {rows}
    </table>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Sản phẩm đồng giá", noi_dung)


# ----------------------------------------------------------
# ĐƠN HÀNG
# ----------------------------------------------------------
@app.route("/donhang")
def hienthi_donhang():
    rows = ""
    for dh in quanly.dsdonhang:
        rows += f"""
        <tr>
            <td>{dh.ma}</td>
            <td>{dh.ten}</td>
            <td>{dh.makhachhang}</td>
            <td>{dh.masanpham}</td>
            <td>{dh.soluong}</td>
            <td>{dh.dathanhtoan}</td>
        </tr>
        """

    noi_dung = """
    <h2>DANH SÁCH ĐƠN HÀNG</h2>
    <table>
        <tr>
            <th>Mã</th><th>Tên</th><th>Mã khách hàng</th>
            <th>Mã sản phẩm</th><th>Số lượng</th><th>Đã thanh toán</th>
        </tr>
    """ + rows + """
    </table>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Đơn hàng", noi_dung)


@app.route("/donhang/them", methods=["GET", "POST"])
def them_donhang():
    if request.method == "POST":
        ma = request.form["ma"]
        ten = request.form["ten"]
        makhachhang = request.form["makhachhang"]
        masanpham = request.form["masanpham"]
        soluong = int(request.form["soluong"])
        dathanhtoan = float(request.form["dathanhtoan"])

        dh = DonHang(
            ma, ten, makhachhang,
            masanpham, soluong, dathanhtoan
        )

        sql = """
            INSERT INTO donhang
            (ma, ten, makhachhang, masanpham, soluong, dathanhtoan)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = quanly.conn.cursor()
        try:
            cursor.execute(sql, (
                dh.ma, dh.ten, dh.makhachhang,
                dh.masanpham, dh.soluong, dh.dathanhtoan
            ))
            quanly.conn.commit()
            quanly.dsdonhang.append(dh)
        finally:
            cursor.close()

        return redirect(url_for("hienthi_donhang"))

    noi_dung = """
    <h2>THÊM ĐƠN HÀNG</h2>
    <form method="post">
        Mã đơn hàng:<br><input name="ma" required>
        Tên đơn hàng:<br><input name="ten" required>
        Mã khách hàng:<br><input name="makhachhang" required>
        Mã sản phẩm:<br><input name="masanpham" required>
        Số lượng:<br><input name="soluong" type="number" required>
        Đã thanh toán:<br><input name="dathanhtoan" type="number" step="any" required>
        <button type="submit">Thêm đơn hàng</button>
    </form>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Thêm đơn hàng", noi_dung)


# ----------------------------------------------------------
# DOANH THU
# ----------------------------------------------------------
@app.route("/doanhthu")
def doanhthu_web():
    rows = ""
    for dh in quanly.dsdonhang:
        doanhthu = quanly.tinhdoanhthudonhang(dh)
        loinhuan = quanly.tinhloinhuandonhang(dh)
        rows += f"""
        <tr>
            <td>{dh.ma}</td>
            <td>{dh.masanpham}</td>
            <td>{dh.soluong}</td>
            <td>{doanhthu}</td>
            <td>{loinhuan}</td>
        </tr>
        """

    noi_dung = f"""
    <h2>DOANH THU</h2>
    <table>
        <tr>
            <th>Mã đơn</th><th>Mã sản phẩm</th><th>Số lượng</th>
            <th>Doanh thu</th><th>Lợi nhuận</th>
        </tr>
        {rows}
    </table>
    <div class="box">
        <b>Tổng doanh thu:</b> {quanly.tongdoanhthu()} VNĐ<br>
        <b>Tổng lợi nhuận:</b> {quanly.tongloinhuan()} VNĐ
    </div>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Doanh thu", noi_dung)


@app.route("/doanhthu/sanpham")
def doanhthu_sanpham_web():
    ketqua = {}
    for dh in quanly.dsdonhang:
        doanhthu = quanly.tinhdoanhthudonhang(dh)
        if dh.masanpham in ketqua:
            ketqua[dh.masanpham] += doanhthu
        else:
            ketqua[dh.masanpham] = doanhthu

    rows = ""
    for masp, doanhthu in ketqua.items():
        sp = quanly.laysanpham(masp)
        if sp is not None:
            rows += f"<tr><td>{sp.ma}</td><td>{sp.ten}</td><td>{doanhthu}</td></tr>"

    noi_dung = f"""
    <h2>DOANH THU THEO SẢN PHẨM</h2>
    <table>
        <tr><th>Mã sản phẩm</th><th>Tên sản phẩm</th><th>Doanh thu</th></tr>
        {rows}
    </table>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Doanh thu theo sản phẩm", noi_dung)


@app.route("/doanhthu/caonhat")
def doanhthu_cao_nhat_web():
    ketqua = {}
    for dh in quanly.dsdonhang:
        doanhthu = quanly.tinhdoanhthudonhang(dh)
        if dh.masanpham in ketqua:
            ketqua[dh.masanpham] += doanhthu
        else:
            ketqua[dh.masanpham] = doanhthu

    if not ketqua:
        noi_dung = "<h2>SẢN PHẨM DOANH THU CAO NHẤT</h2><p>Chưa có dữ liệu!</p>"
    else:
        mamax = max(ketqua, key=ketqua.get)
        sp = quanly.laysanpham(mamax)
        noi_dung = f"""
        <h2>SẢN PHẨM DOANH THU CAO NHẤT</h2>
        <div class="box">
            <b>Sản phẩm:</b> {sp.ten if sp else mamax}<br>
            <b>Doanh thu:</b> {ketqua[mamax]} VNĐ
        </div>
        """

    noi_dung += '<a class="back" href="/">← Về menu chính</a>'
    return khung_trang("Doanh thu cao nhất", noi_dung)


# ----------------------------------------------------------
# THỐNG KÊ
# ----------------------------------------------------------
@app.route("/thongke")
def thongke_web():
    noi_dung = f"""
    <h2>THỐNG KÊ CÔNG TY ABC</h2>
    <div class="box">
        Số khách hàng: <b>{len(quanly.dskhachhang)}</b><br><br>
        Số sản phẩm: <b>{len(quanly.dssanpham)}</b><br><br>
        Số đơn hàng: <b>{len(quanly.dsdonhang)}</b><br><br>
        Tổng doanh thu: <b>{quanly.tongdoanhthu()} VNĐ</b><br><br>
        Tổng lợi nhuận: <b>{quanly.tongloinhuan()} VNĐ</b>
    </div>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Thống kê", noi_dung)


# ----------------------------------------------------------
# CÔNG NỢ
# ----------------------------------------------------------
@app.route("/congno")
def congno_web():
    noi_dung = f"""
    <h2>TỔNG CÔNG NỢ</h2>
    <div class="box">
        Tổng công nợ: <b>{quanly.tongcongno()} VNĐ</b>
    </div>
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Tổng công nợ", noi_dung)


@app.route("/congno/khachhang", methods=["GET", "POST"])
def congno_khachhang_web():
    ketqua = ""
    if request.method == "POST":
        makh = request.form["makh"]
        tong = 0
        co_don = False
        rows = ""

        for dh in quanly.dsdonhang:
            if dh.makhachhang == makh:
                co_don = True
                sp = quanly.laysanpham(dh.masanpham)
                if sp is None:
                    continue

                thanhtien = dh.soluong * sp.giaban
                congno = thanhtien - dh.dathanhtoan
                tong += congno

                rows += f"""
                <tr>
                    <td>{dh.ma}</td>
                    <td>{sp.ten}</td>
                    <td>{dh.soluong}</td>
                    <td>{thanhtien}</td>
                    <td>{dh.dathanhtoan}</td>
                    <td>{congno}</td>
                </tr>
                """

        if co_don:
            ketqua = f"""
            <table>
                <tr>
                    <th>Mã đơn</th><th>Sản phẩm</th><th>Số lượng</th>
                    <th>Thành tiền</th><th>Đã thanh toán</th><th>Công nợ</th>
                </tr>
                {rows}
            </table>
            <div class="box"><b>Tổng công nợ:</b> {tong} VNĐ</div>
            """
        else:
            ketqua = "<p>Khách hàng này chưa có đơn hàng!</p>"

    noi_dung = f"""
    <h2>CÔNG NỢ CỦA TỪNG KHÁCH HÀNG</h2>
    <form method="post">
        Mã khách hàng:<br><input name="makh" required>
        <button type="submit">Tính công nợ</button>
    </form>
    {ketqua}
    <a class="back" href="/">← Về menu chính</a>
    """
    return khung_trang("Công nợ khách hàng", noi_dung)


# ==========================================================
# CHẠY WEBSITE
# ==========================================================
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
