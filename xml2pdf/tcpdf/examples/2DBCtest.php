<?php

date_default_timezone_set('America/Los_Angeles');

//read xml

require_once('tcpdf/tcpdf.php');

//-------------------------------------------------------------------------------------
// create new PDF document
$pdf = new TCPDF('portrait', 'mm', 'A4', true, 'UTF-8', false);

$pdf->AddPage();

//generate form

$style2Dcode = array(
    'border'   => false,
    'vpadding' => 0,
    'hpadding' => 0,
    'fgcolor'  => array(0,0,0),
    'bgcolor'  => false,  //array(255,255,255)
    'module_width'  => 1, // width of a single module in points
    'module_height' => 1  // height of a single module in points
);

// 2D barcodes on page:
$content = "CHE:001:56:2013031323433245:$rectangle_2_metrics:50,110,237/3,70/3";

$pdf->write2DBarcode($content, 'DATAMATRIX', 185,  15, 10, 10, $style2Dcode, 'N', $distort="true");
$pdf->write2DBarcode($content, 'DATAMATRIX',  10, 260, 10, 10, $style2Dcode, 'N', $distort="true");
$pdf->write2DBarcode($content, 'DATAMATRIX', 185,  25, 10, 10, $style2Dcode, 'N', $distort="true");
$pdf->write2DBarcode($content, 'DATAMATRIX',  25, 260, 10, 10, $style2Dcode, 'N', $distort="true");

$pdf->SetDrawColor(50, 0, 0, 0);
$pdf->SetAlpha(0.31);
$pdf->Rect(185,  15, 10, 10,'',$border_style=array(0),$fill_color=array());
$pdf->Rect( 10, 260, 10, 10,'',$border_style=array(0),$fill_color=array());
$pdf->Rect(185,  25, 10, 10,'',$border_style=array(0),$fill_color=array());
$pdf->Rect( 25, 260, 10, 10,'',$border_style=array(0),$fill_color=array());
$pdf->SetAlpha(1);

$pdf->Output('test.pdf', 'F');

?>
