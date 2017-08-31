function printDiv(divName) {
    var printContents = document.getElementById(divName).innerHTML;
    w = window.open();
    w.document.write(printContents);
    w.print();
    w.close();
};


// <!-- <script type="text/javascript">
// function printDiv(divName) {
//     var printContents = document.getElementById(divName).innerHTML;
//     w = window.open();
//     w.document.write(printContents);
//     w.print();
//     w.close();
// }
// </script> -->