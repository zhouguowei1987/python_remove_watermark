# -*- coding:utf-8 -*-
# @Time   : 2022-02-23
# @Author : carl_DJ
import json

import fitz
import os


# 去除pdf的水印
def remove_pdf_watermark():
    subject_dirs_arr = ['学历类', '职业资格', '公务员', '医卫类', '建筑工程', '外语类', '外贸类', '计算机类', '财会类', '技能鉴定']
    root_dir = "../bilianku.com"
    subject_dirs = sorted(os.listdir(root_dir))
    for subject in subject_dirs:
        if subject in subject_dirs_arr:
            category_dirs = sorted(os.listdir(root_dir + "/" + subject))
            for category in category_dirs:
                files = sorted(os.listdir(root_dir + "/" + subject + "/" + category))
                for file in files:
                    if ".pdf" in file:
                        pdf_file = root_dir + "/" + subject + "/" + category + "/" + file
                        print(pdf_file)
                        try:
                            doc = fitz.open(pdf_file)

                            if len(doc[0].get_text('dict')) <= 0:
                                print("删除文件")
                                os.remove(pdf_file)
                                continue

                            pdf_new_dir = '../finish-bilianku.com' + "/" + subject + "/" + category
                            if not os.path.exists(pdf_new_dir):
                                os.makedirs(pdf_new_dir)

                            pdf_new_file = pdf_new_dir + "/" + file
                            for pno in range(doc.page_count):
                                page = doc[pno]
                                page.clean_contents()
                                xref = page.get_contents()[0]
                                cont = bytearray(page.read_contents())

                                i1 = cont.find(b'w\n/Im1')
                                if i1 < 0:
                                    break
                                start_i1 = cont.rfind(b'd\nq\nq\n', 0, i1)

                                i2 = cont.find(b"Do\nQ\nQ\n[]", i1)
                                cont[start_i1: i2 + 9] = b""
                                doc.update_stream(xref, cont)
                            if os.path.exists(pdf_new_file):
                                os.remove(pdf_new_file)
                            doc.save(pdf_new_file)
                            doc.close()
                            exit(1)
                        except Exception as e:
                            print(e)
                            print("删除文件")
                            os.remove(pdf_file)


if __name__ == '__main__':
    remove_pdf_watermark()
