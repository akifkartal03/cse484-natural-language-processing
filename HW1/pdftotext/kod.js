var pdfUtil = require("pdf-to-text");
const fs = require("fs-extra");

let books = [
  { path: "./books/cografya_1.pdf", option: { from: 15, to: 180 } },
  { path: "./books/cografya_2.pdf", option: { from: 15, to: 80 } },
  { path: "./books/cografya_3.pdf", option: { from: 15, to: 180 } },
  { path: "./books/cografya_4.pdf", option: { from: 15, to: 160 } },
  { path: "./books/cografya_5.pdf", option: { from: 15, to: 225 } },
  { path: "./books/cografya_6.pdf", option: { from: 15, to: 170 } },
  { path: "./books/cografya_7.pdf", option: { from: 15, to: 115 } },
  { path: "./books/biyoloji_1.pdf", option: { from: 15, to: 75 } },
  { path: "./books/biyoloji_2.pdf", option: { from: 15, to: 60 } },
  { path: "./books/biyoloji_3.pdf", option: { from: 15, to: 70 } },
  { path: "./books/biyoloji_4.pdf", option: { from: 15, to: 80 } },
  { path: "./books/biyoloji_5.pdf", option: { from: 15, to: 160 } },
  { path: "./books/biyoloji_6.pdf", option: { from: 15, to: 115 } },
  { path: "./books/biyoloji_8.pdf", option: { from: 15, to: 90 } },
  { path: "./books/tarih_2.pdf", option: { from: 15, to: 110 } },
  { path: "./books/tarih_3.pdf", option: { from: 15, to: 110 } },
  { path: "./books/tarih_4.pdf", option: { from: 15, to: 75 } },
  { path: "./books/tarih_5.pdf", option: { from: 15, to: 225 } },
  { path: "./books/inkilap_tarihi_1.pdf", option: { from: 15, to: 255 } },
  { path: "./books/edebiyat_5.pdf", option: { from: 15, to: 110 } },
  { path: "./books/edebiyat_6.pdf", option: { from: 15, to: 80 } },
  { path: "./books/edebiyat_7.pdf", option: { from: 15, to: 110 } },
  { path: "./books/edebiyat_8.pdf", option: { from: 15, to: 155 } },
];

/*
let sum = 0, i = 0;
for (const book of books) {
  sum = sum + (book.option.to - book.option.from);
  i++;
}
console.log("total number of book: " + i);
console.log("total number of page: " + sum);*/
let i = 0;

function convertFiles(book) {
  pdfUtil.pdfToText(book.path, book.option, function (err, data) {
    //console.log(book.path);
    if (err) {
      console.log(book.path);
      throw err;
    }
    try {
      const found = data.replace(/\s+/g, " ").replaceAll("..", "");
      const foundtr = found.toLocaleLowerCase("tr");
      //const foundtr2 = foundtr.replace(re,"");
      fs.appendFile("sample36.txt", foundtr, (err) => {
        if (err) throw err;
        //console.log(book.path + "\n");
        console.log(i);
        i++;
      });
    } catch (error) {
      console.error(error);
    }
  });
}

for (const book of books) {
  convertFiles(book);
}
