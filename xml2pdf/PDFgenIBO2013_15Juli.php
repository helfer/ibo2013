#!/usr/bin/php
<?php
// The PDF output of this script is not clean and only ment for printing.

// check TCPDF examples 8 and 18 for language problems

// THESE VALUES HAVE TO BE ADJUSTED FOR THE ENVIRONMENT
$return_filename = "yes"; // "yes" or "no". if 'yes' "PDFfilename: Exam_name-FOR TRANSLATION INTO-targetLanguage-FROM-primaryLanguage.pdf" is written to STDOUT
$path_to_images_folder = 'images'; // Full or relative path to the folder containing the image files
$path_to_tcpdf = 'tcpdf/tcpdf.php'; // Full or relative path to 'tcpdf.php'
$php_timezone = 'America/Los_Angeles'; // Time zone

// SCRIPT OPTIONS
//PDF FOR TRANSLATION: 1, DRAFT PDF: 0
$TRANSLALTION            = 0;
// Verbose synthax: 0=quiet, 1=display errors, 2=display verbose output
$verboseXML              = 1;
$verboseTranslationBox   = 1;
$verboseTranslationFig   = 1;
$verboseTranslationTable = 1;
$verboseSVGtoPNG         = 1;

// PDF OPTIONS 
// The multipier values say how may mm height schould be added for one char in text
$pdf_left_margin      = 22;
$pdf_top_margin       = 22;
$pdf_bottom_margin    = 22;
$barcode_sides_lenght =  9;
$translation_box_boarder_grey_value = 192; // grey value of the handwriting scanbox border : 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224 // websafe colors: www.w3schools.com/html/html_colors.asp
$translation_box_boarder_width      =   1; // in PDFs standard unit, here this should mean 'mm'

// DISPLAY SPECIFIC VALUES
// Define the width of the different panels where the pictures are shown
$left_panel_width           =  150;
$left_panel_list_width      =  130;
$right_panel_width          =   67; 
$answersplit_width          =   30;
$left_panel_multiplier      =    0.15;
$left_panel_list_multiplier =    0.15;
$right_panel_multiplier     =    0.3 ;
$answersplit_multiplier     =    0.3 ;


// SCRIPT INTERN VALUES
$TEST_COLOR = "#00FF00";
$FILES_TO_UNLINK_UPON_SUCCESSFUL_COMPLETION = array();

// Set timezone
date_default_timezone_set($php_timezone);
require_once($path_to_tcpdf);

class ibo2013PDFtranslation extends TCPDF{	
	
	public function __construct($title) {
       parent::__construct('portrait', 'mm', 'A4', true, 'UTF-8', false);       

		// set document information
		$this->SetCreator(PDF_CREATOR);
		$this->SetAuthor('PDFgenIBO2013.php');
		$this->SetTitle($title);
				      
		global $pdf_left_margin;
		global $pdf_top_margin;
		global $pdf_bottom_margin;
		$this->SetMargins($pdf_left_margin, $pdf_top_margin); //left, top, right == left
		
		//set auto page breaks
		$this->SetAutoPageBreak(TRUE, $pdf_bottom_margin); // number is the bottom page boarder in mm
		
		//set default font
		$this->setDefaultFont(); 
		
		// set default font subsetting mode
		$this->setFontSubsetting(true);
		
   }
	
	public function AddPageIBO(){
		global $pdf_left_margin;
		global $pdf_top_margin;
		$this->AddPage();
		$this->SetX($pdf_left_margin);
		$this->SetY($pdf_top_margin);
	}
	
	public function AddTranslationPageIBO(){
		global $pdf_left_margin;
		global $pdf_top_margin;
		$this->AddPage();
		$this->SetX($pdf_left_margin);
		$this->SetY($pdf_top_margin);
	}
	
	public function setDefaultFont(){
		//$this->SetFont('times', '', 12, '', true);
		$this->SetFont('helvetica', '', 12, '', true);
	}
	
	public function Header() {		
		global $TRANSLALTION;
		
		if($this->numpages == 1){
			//add Logo
			//$this->ImageSVG($file=getcwd().'/images/Logo_IBO2013_CMYK_Off.svg', $x=20.7, $y=16, $w=64.6, $h='', $link='http://www.ibo2013.org', $align='', $palign='');
		} else {
			//add name only
			//$this->ImageSVG($file=getcwd().'/images/Logo_IBO2013_name_only_Off_pdf14.svg', $x=20.7, $y=16, $w=64.6, $h='', $link='http://www.ibo2013.org', $align='', $palign='');			
			//and add page number in front			
			/*$this->SetFont('times', '', 12, '', true);
			$this->SetX(-50);
			$this->SetY(26);
			$this->Cell(10, 10, $this->getAliasNumPage().'  | ', 0, 1, 'R', 0, '', 0);*/
		}
		
		if ($TRANSLALTION == 1) {
			$this->SetFont('times', '', 12, '', true);
			$this->SetX(0);
			$this->SetY(15);
			$this->Cell(0, 0, $this->getAliasNumPage().'  | IBO2013 '. $this->title, 0, 1, 'L', 0, '', 0);
		
			/* 
			 2D barcodes might be paced into the background not to cause any unwanted page-breaks 
			*/
		
			global $barcode_sides_lenght;
			global $exam_name;
			$barcode_info_string = $exam_name;
			// set the page orientation barcodes
		
			$style2Dcode = array(
				'border'   => false,
				'vpadding' => 0,
				'hpadding' => 0,
				'fgcolor'  => array(0,0,0),
				'bgcolor'  => false,  //array(255,255,255)
				'module_width'  => 1, // width of a single module in points
				'module_height' => 1  // height of a single module in points
			);
		
			$barcode_x_offset_l   = 10; // offset for placing 2D code on the left of the page
			$barcode_x_offset_r   = False; // offset for placing 2D code on the left of the page
			$barcode_y_offset_t   = 12; // offset for placing 2D code on the top of the page
			$barcode_y_offset_b   = 278; // offset for placing 2D code on the bottom of the page
			//$barcode_y_offset_b    = 300;// breaks test
		
			// barcode top left center
			$barcode_x_center_tl    = $barcode_x_offset_l + ( $barcode_sides_lenght/2 );
			$barcode_y_center_tl    = $barcode_y_offset_t + ( $barcode_sides_lenght/2 );
			// barcode bottom right center
			$barcode_x_center_bl    = $barcode_x_offset_l + ( $barcode_sides_lenght/2 );
			$barcode_y_center_bl    = $barcode_y_offset_b + ( $barcode_sides_lenght/2 );
		
			$top_left_barcode_string 	=	'olt' .
											',' . $barcode_x_center_tl . 
											',' . $barcode_y_center_tl . 
											':' . $barcode_info_string; // tl for top left
			$bottom_left_barcode_string = 	'olb' .
											',' . $barcode_x_center_bl . 
											',' . $barcode_y_center_bl . 
											':' . $barcode_info_string; // bl for bottom left

			extract($this->getMargins(),EXTR_PREFIX_ALL,"margin"); // -> $margin_left, $margin_right, $margin_top, $margin_bottom
		
			// test the barcode coordiantes of their validity (10 units inside the page)
			$tests_passed = 1; // set default
			$reqired_distance_from_page_edge = 8; // could be $margin_bottom or $margin_right
		
			// test page width and right margin
			if ($this->getPageWidth() < (max($barcode_x_offset_l, $barcode_x_offset_r) + $barcode_sides_lenght + $reqired_distance_from_page_edge) ) {
				$tests_passed = 0;
			}
			// test page height and Breakmargin
			if ($this->getPageHeight() < (max($barcode_y_offset_t, $barcode_y_offset_b) + $barcode_sides_lenght + $reqired_distance_from_page_edge) ) {
				$tests_passed = 0;
			}
		
			// get the current page break margin
			$bMargin = $this->getBreakMargin();
			// get current auto-page-break mode
			$auto_page_break = $this->getAutoPageBreak();
			// disable auto-page-break
			$this->SetAutoPageBreak(false, 0);
		
			// set the 2D barcodes
			if ($tests_passed == 1) {
				$this->write2DBarcode($top_left_barcode_string, 'DATAMATRIX', $barcode_x_offset_l, $barcode_y_offset_t, $barcode_sides_lenght, $barcode_sides_lenght, $style2Dcode, 'N', $distort="true");
				$this->write2DBarcode($bottom_left_barcode_string, 'DATAMATRIX', $barcode_x_offset_l, $barcode_y_offset_b, $barcode_sides_lenght, $barcode_sides_lenght, $style2Dcode, 'N', $distort="true");
			} else {
				// Start Transformation
				$this->StartTransform();
				// Rotate 54 degrees counter-clockwise centered by (70,110) which is the lower left corner of the rectangle
				//$this->Rotate(54, 20, 27);
				$this->ScaleXY(200,  0,  -10);
				$this->SetDrawColor( 40, 40, 40,  0);
				$this->SetAlpha(0.41);
				$test_fail_text_single = 'DO NOT USE THIS DOCUMENT FOR TRANSLATION! Please report the error.';
				$test_fail_text = str_repeat($test_fail_text_single,1);
				$this->Text(0,   0, $test_fail_text);
				$this->Text(0,  20, $test_fail_text);
				$this->Text(0,  40, $test_fail_text);
				$this->Text(0,  60, $test_fail_text);
				$this->Text(0,  80, $test_fail_text);
				$this->Text(0, 100, $test_fail_text);
				$this->Text(0, 120, $test_fail_text);
				$this->Rect( $barcode_x_offset_l, 120, $barcode_sides_lenght, 300, '', $border_style=array(0), $fill_color=array());
				$this->SetAlpha(1);
				$this->SetDrawColor(0, 0, 255);
				// Stop Transformation
				$this->StopTransform();
			}
		
			// restore auto-page-break status
			$this->SetAutoPageBreak($auto_page_break, $bMargin);
			// set the starting point for the page content
			//$this->setPageMark();
			$this->writeHTMLCell(0, 0, $margin_left, $margin_top);
		}
	}
	
	public function Footer() {
		$cur_y = $this->getY();		
		$this->ImageSVG($file=getcwd().'/images/Adresszeile.svg', $x=23, $y=279, $w=167, $h='', $link='http://www.ibo2013.org', $align='', $palign='');
		$this->SetY($cur_y);		
	}
	
	public function HandwritingScanBox ($tl_x_scanbox,$tl_y_scanbox,$width,$height,$fragment_info,$visibility) {
		global $barcode_sides_lenght;
		global $translation_box_boarder_grey_value;
		global $translation_box_boarder_width;
		global $exam_name;
		global $exam_date;
		global $exam_time;
		global $exam_primary_l;
		global $exam_primary_language_id;
		global $exam_target_language;
		global $exam_target_language_id;


		$spacer = 2; // space between box and 2D code in mm
		
		// to round the values at this point could lead to unexpected translation box placement
		//    cuts the number after two digits behind the point
		$tl_x_scanbox = floor($tl_x_scanbox*10)/10;
		$tl_y_scanbox = floor($tl_y_scanbox*10)/10;
		
		extract($this->getMargins(),EXTR_PREFIX_ALL,"margin"); // -> $margin_left, $margin_right, $margin_top, $margin_bottom
		
		if($width == 0) {
			$width = $this->getPageWidth() - $margin_left - $margin_right;
		}
		
		$min_height = 10;// This should not be smaller than the barcode side length
		if($height < $min_height) {
			$height = $min_height;
		}
		
		$style2Dcode = array(
			'border'   => false,
			'vpadding' => 0,
			'hpadding' => 0,
			'fgcolor'  => array(0,0,0),
			'bgcolor'  => false,  //array(255,255,255)
			'module_width'  => 1, // width of a single module in points
			'module_height' => 1  // height of a single module in points
		);
		
		// barcode top left center
		$barcode_x_center_ul    = $tl_x_scanbox - $spacer - ( $barcode_sides_lenght/2 );
		$barcode_y_center_ul    = $tl_y_scanbox + ( $barcode_sides_lenght/2 );
		// barcode bottom right center
		$barcode_x_center_lr    = $tl_x_scanbox + $width + $spacer + ( $barcode_sides_lenght/2 );
		$barcode_y_center_lr    = $tl_y_scanbox + $height - $barcode_sides_lenght + ( $barcode_sides_lenght/2 );
		
		// barcode content (q_id-info_id-fragment_id-tlx-tly-width-height-position)
		$barcode_string = $fragment_info . ':' . $tl_x_scanbox . ',' . $tl_y_scanbox . ',' . $width . ',' . $height;
		$upper_left_barcode_string  = $barcode_string . ':ul'; // ul for upper left
		$lower_right_barcode_string = $barcode_string . ':lr'; // br for lower right
										
		// add translation rectangle
		//$style_invisible = array('width' => $translation_box_boarder_width, 'cap' => 'butt', 'join' => 'miter', 'dash' => 0, 'color' => array(255, 0, 0));
		$style_visible   = array('width' => $translation_box_boarder_width, 'cap' => 'butt', 'join' => 'miter', 'dash' => 0, 'color' => array($translation_box_boarder_grey_value, $translation_box_boarder_grey_value, $translation_box_boarder_grey_value));
		$style_invisible = array('width' => $translation_box_boarder_width, 'cap' => 'butt', 'join' => 'miter', 'dash' => 0, 'color' => array(255, 255, 255));
		
		if($visibility == 0) {
			
			$this->Rect($tl_x_scanbox,
						$tl_y_scanbox,
						$width,
						$height, 
						'D',
						$border_style=array('all' => $style_invisible), 
						$fill_color=array());
					
			// add "new line" after tranlation box (adds vertical space and resets x-value)
			$this->Ln(1);
		} 
		elseif($visibility == 1) {
		
			$this->Rect($tl_x_scanbox,
						$tl_y_scanbox,
						$width,
						$height, 
						'D',
						$border_style=array('all' => $style_visible), 
						$fill_color=array());
		
			$dummy = 0;
			if ($dummy == 1) {
				// add dummy handwriting
				$this->Image(	$file=getcwd().'/images/handwriting-lined.jpg', 
								$tl_x_scanbox + 1,
								$tl_y_scanbox + 1,
								$width - 2,
								$height - 2,
								'', '', '', true);
			}
			
			// add info next to translation box
			$tl_x_infobox = $tl_x_scanbox + $width + 2 * $spacer + $barcode_sides_lenght;
			$tl_y_infobox = $tl_y_scanbox;
			
			//echo $fragment_info . "\n";
			
			$info_text = str_replace('-',"\n",$fragment_info);
			
			//echo $info_text . "\n";
			$this->MultiCell(  30,  0,       $info_text       , 0, 'J', 0, 1, $tl_x_infobox, $tl_y_infobox, true, 0, false, true,  9, 'T', true);
			//$this->MultiCell(55, 60, '[FIT CELL] '.$txt."\n", 1, 'J', 1, 1,           125,           145, true, 0, false, true, 60, 'M', true);
			
			// add barcodes left and right to the box
			$this->write2DBarcode(
				$upper_left_barcode_string, 'DATAMATRIX', 
				$tl_x_scanbox - ($barcode_sides_lenght + $spacer), 
				$tl_y_scanbox,
				$barcode_sides_lenght,
				$barcode_sides_lenght, $style2Dcode, 'N', $distort="true");
			
			$this->write2DBarcode(
				$lower_right_barcode_string, 'DATAMATRIX',
				$tl_x_scanbox + $width + $spacer,
				$tl_y_scanbox + $height - $barcode_sides_lenght,
				$barcode_sides_lenght,
				$barcode_sides_lenght, $style2Dcode, 'N', $distort="true");
			
			// add "new line" after tranlation box (adds vertical space and resets x-value)
			$this->Ln(1);
		} else {
			echo "ERROR: illegal value for visibility.";
		}
	}
	
	public function writeHTMLLeft($html, $x=0, $y=0){		
		$this->writeHTMLCell($w=0, $h=0, $x=$this->lMargin+$x, $y=$this->y+$y, $html, $border=0, $ln=1, $fill=0, $reseth=true, $align='', $autopadding=true);
	}
	
	public function writeHTMLMultiCellLeft($html, $x=0, $y=0){		
		$this->writeHTMLCell($w=0, $h=0, $x=$this->lMargin+$x, $y=$this->y+$y, $html, $border=0, $ln=1, $fill=0, $reseth=true, $align='', $autopadding=true);
	}
	
}



// start processing pipe from stdin
$handle = fopen('php://stdin', 'r');
$xml_str = '';
do {
    $buffer = fgets($handle);
    $xml_str .= $buffer;
} while(!feof($handle));
fclose($handle);


//$xml_str = file_get_contents('xmlfile.xml');// XML file input 
$exam_xml = new SimpleXMLElement($xml_str);

echo ($verboseXML > 1) ? $exam_xml->getName() . "\n" : '';

$exam_id                  = $exam_xml['id'];
$exam_name                = $exam_xml['name'];
$exam_date                = $exam_xml['date'];
$exam_time                = $exam_xml['time'];
$exam_primary_language    = $exam_xml['primaryLanguage'];
$exam_primary_language_id = $exam_xml['primaryLanguageId'];
$exam_target_language     = $exam_xml['targetLanguage'];
$exam_target_language_id  = $exam_xml['targetLanguageId'];

if ($exam_target_language && $exam_target_language_id) {
	$pdf_title = $exam_name . '_source_' . $exam_primary_language_id . '_target_' . $exam_target_language_id;
	$pdf_filename = './output/'.$argv[1];
	$TRANSLALTION = 1;
} 
else {
	$pdf_title = $argv[1] . '- DRAFT';
	$pdf_filename = './output/'.$argv[1];
	$TRANSLALTION = 0;
}

//print "translation: $TRANSLALTION\n";

if ($return_filename == "yes") {
	echo "PDFfilename: " . $pdf_filename . "\n";
}

$pdf = new ibo2013PDFtranslation($pdf_title);
$lg['a_meta_charset'] = 'UTF-8';
$pdf->setLanguageArray($lg);
//$pdf->SetFont('helvetica', '', 12);
$pdf->SetFont('dejavusans', '', 12);
//$fontname = $pdf->addTTFfont('./tcpdf/fonts/unifont.ttf', 'GNU unifont', '', 32);
//$pdf->SetFont($fontname, '', 12);

$orientation_content = "$exam_id-$exam_target_language_id";

$namespaces = '';
$q_xml = $exam_xml->asXML();


$pos = mb_strpos($q_xml,'>');
#print mb_substr($q_xml,0,mb_strpos($q_xml,'>',$pos+1));
$q_xmlns_array = explode(' ', mb_substr($q_xml,0,mb_strpos($q_xml,'>',$pos+1)));
foreach($q_xmlns_array as $k){
	$x = explode(':',$k);
	if ($x[0] == 'xmlns') {
		$namespaces .= ' ' . $k ;
	}
}

foreach($exam_xml as $child) {
	if ( $child->getName() == 'question') {
		$pdf->AddTranslationPageIBO();
		exam_question($child);
	} else {
		echo ($verboseXML > 1) ? "Found exam child that is not 'question' but " . $child . ". Not allowed. Too easy :) \n" : '';
	}
}

//echo $pdf_filename;
$pdf->Output($pdf_filename, 'F');



foreach ($FILES_TO_UNLINK_UPON_SUCCESSFUL_COMPLETION as $file_fo_unlink) {
	unlink($file_fo_unlink);
}







function exam_question ($question_xml) {
	global $exam_xml;
	global $verboseXML;
	global $pdf;
	global $TRANSLALTION;
	
	/*
	// test if the formating itself cases the vertical text shift at the problem. it does not.
	$html = "<b>1</b> = a<sup>2</sup> + K<sub>2</sub> - <i>i</i>";
	$html .= "Indicate for each of the following statements if it is <b>true</b> or false.";
	$pdf->writeHTMLLeft($html);
	//$pdf->writeHTML($html);
	*/
	
	$question_info['id']             = $question_xml['id'];
	$question_info['info']           = $question_xml['info'];
	$question_info['position']       = $question_xml['position'];
	$question_info['primaryVersion'] = $exam_xml['primaryLanguageId'];
	$question_info['targetVersion']  = $exam_xml['targetLanguageId'];
	
	$html = '<h2>Question ';
	$html .= $question_info['position'];
	if ($TRANSLALTION == 1) {
		$html .= ' source ';
		$html .= $question_info['primaryVersion'];
		$html .= ' target ';
		$html .= $question_info['targetVersion'];
	}
	$html .= '</h2>';
	$pdf->writeHTMLLeft($html);
	//$pdf->writeHTML($html);
	
	echo ($verboseXML > 1) ? $question_xml->getName() . ":\n"  : '';
	foreach ($question_xml->children() as $question_child) {
		$q_child_name = $question_child->getName();
		switch ($q_child_name) {
			case 'text'      : exam_text($question_child, $question_info)      ; break;
			case 'task'      : exam_task($question_child, $question_info)      ; break;
			case 'list'      : exam_list($question_child, $question_info)      ; break;
			case 'table'     : exam_table($question_child, $question_info)     ; break;
			case 'figure'    : exam_figure($question_child, $question_info)    ; break;
			case 'answerlist': exam_answerlist($question_child, $question_info); break;
            case 'comment'   : exam_comment($question_child, $question_info)   ; break;
			default          : echo ($verboseXML > 0) ? "ERROR: Found question child that is unknown: " . $q_child_name . ". Find out why.\n" : ''; break;
		}
	}
}

function exam_text ($text_xml, $question_info) {
	global $verboseXML;
	global $pdf;
	global $left_panel_width;
	global $right_panel_width;
	global $TRANSLALTION;
	
	$question_fragment_id = $text_xml['id'];
	
	echo ($verboseXML > 1) ? "  " . $text_xml->getName() . ": " . $text_xml . "\n" : '';
	
	$text = $text_xml->asXML();
	$text = preg_replace(':.+?\>(.+)</.+:s','$1',$text); // strip preciding and trailing xml tags from html content
	$html = tex_to_html($text);
	
	if ($TRANSLALTION == 1) {
		translation_box($left_panel_width, $text, $html, $question_info, $question_fragment_id);
	}
	else {
		$height = getheight_writeHTMLLeft($html);
		$pdf->writeHTMLLeft($html);
		//$pdf->writeHTML($html);
		$pdf->Ln(1);
	}
}

function exam_task ($task_xml, $question_info) {
	global $verboseXML;
	global $pdf;
	global $left_panel_width;
	global $right_panel_width;
	global $TRANSLALTION;
	
	$question_fragment_id = $task_xml['id'];
	
	echo ($verboseXML > 1) ? "  " . $task_xml->getName() . ": " . $task_xml . "\n" : '';
	
	$text = $task_xml->asXML();
	$text = preg_replace(':.+?\>(.+)</.+:','$1',$text); // strip preciding and trailing xml tags from html content
	$html = tex_to_html($text);
	$html = "Indicate for each of the following statements if it is <b>true</b> or false.";
	
	if ($TRANSLALTION == 1) {
		translation_box($left_panel_width, $text, $html, $question_info, $question_fragment_id);
	}
	else {
		$pdf->writeHTMLLeft($html);
		//$pdf->writeHTML($html);
		$pdf->Ln(1);
	}
}

function exam_list ($list_xml, $question_info) {
	global $verboseXML;
	global $pdf;
	global $left_panel_width;
	global $right_panel_width;
	global $left_panel_list_width;
	global $TRANSLALTION;
	
	echo ($verboseXML > 1) ? "  " . $list_xml->getName() . ":\n" : '';
	
	foreach ($list_xml as $l_element) {
		$l_element_name = $l_element->getName();
		switch ($l_element_name) {
			case 'item':
				$question_fragment_id = $l_element['id'];
	
				echo ($verboseXML > 1) ? "    " . $l_element_name . ":\n" : '';
				
				$text = $l_element->asXML(); // trip xml tag from html content
				$text = preg_replace(':.+?\>(.+)</.+:','$1',$text); // strip preciding and trailing xml tags from html content
				$html = tex_to_html($text);
	
				if ($TRANSLALTION == 1) {
					translation_box($left_panel_list_width, $text, $html, $question_info, $question_fragment_id);
				}
				else {
					$html = '<ul><li>' . $html . '</li></ul>';
					$pdf->writeHTMLLeft($html);
					//$pdf->writeHTML($html);
					$pdf->Ln(1);
				}
				break;
			default:
				echo ($verboseXML > 0) ? "Undefined list element:" . $l_element_name . ".\n" : '';
		}
	}
}

function exam_table ($table_xml, $question_info) {
	global $verboseXML;
	global $verboseTranslationTable;
	
	echo (($verboseXML > 0) || ($verboseTranslationTable > 0)) ? "ERROR: Found a table. Tables are not allowed and must be transformed to SVG graphics for translation.\n" : '';
	
	echo (($verboseXML > 1) || ($verboseTranslationTable > 1)) ? "Processing SVG tables for translation.\n" : '';
	exam_figure($table_xml, $question_info);
	
	/*
	global $pdf;
	global $left_panel_width;
	global $right_panel_width;
	
	echo ($verboseXML > 1) ? "  " . $table_xml->getName() . ":\n" : '';
	
	$html = '<table border="1" cellspacing="0" cellpadding="1" >';
	
	foreach ($table_xml as $t_element) {
		$html .= '<tr>';
		$t_element_name = $t_element->getName();
		switch ($t_element_name) {
			case 'header':
				echo ($verboseXML > 1) ? "    " . $t_element_name . ":\n" : '';
				$header_cells = $t_element->children();
				foreach ($header_cells as $header_cell) {
					$html .= '<th>' . $header_cell . '</th>';
				}
				break;
			case 'row':
				echo ($verboseXML > 1) ? "    " . $t_element_name . ":\n" : '';
				$row_cells = $t_element->children();
				foreach ($row_cells as $row_cell) {
					$html .= '<td>' . $row_cell . '</td>';
				}
				break;
			default:
				echo ($verboseXML > 0) ? "Undefined table element:" . $t_element_name . ".\n" : '';
		}
		$html .= '</tr>';
	}
	$html .= '</table>';
	
	// write translation table
	translation_table($left_panel_width, $html, $question_info);
	*/
}

function exam_figure ($figure_xml, $question_info) {
	global $namespaces;
	global $verboseXML;
	global $pdf;
	global $left_panel_width;
	global $right_panel_width;
	global $path_to_images_folder;
	global $TRANSLALTION;
	
	$question_fragment_id = $figure_xml['id'];
	$question_fragment_imagefile = $figure_xml['imagefile'];
	
	echo ($verboseXML > 1) ? "  " . $figure_xml->getName() . ": " . $figure_xml . "\n" : '';
	
	$xml_string = $figure_xml->asXML();
	
	$figure_content_string = preg_replace(':.+?\>(.*)</.+:si','$1',$xml_string); // strip preciding and trailing xml tags from html content
	
	if ( isset($figure_xml->svginline) ) {
		$svginline_xml = $figure_xml->svginline->asXML(); // => <svginline> <svg> ... </svg> </svginline>
		//print_r($svginline_xml);
		$svg_content_string = preg_replace(':.+?\>(.+)</.+:s','\1',$svginline_xml); // => <nsX:svg> ... </nsX:svg>
		// $svg_content_string = preg_replace("/(<ns0:text((?!<\/text>).)+?id=\"$ta_id.+?<ns0:tspan>).+(<\/ns0:tspan><\/ns0:text>)/si", "\1$ta_text\\4", $svg_content_string);// tspan
	} else {
		if( preg_match("/(<.*?svg[^<]+<\/.*?svg>)/si", $figure_content_string, $match)  ) {
					$svg_content_string = $match[1];
		}
		else {
			$figure_file = $figure_xml['imagefile'];
			$figure_with_path = $path_to_images_folder . "/" . $figure_file;
			if ($svgimg = file_get_contents($figure_with_path)) {
				if ( preg_match('/(<svg.+svg>)/si', $svgimg, $match)) {
					$svg_content_string = $match[1];
				}
			} 
			else {
				echo ($verboseXML > 0) ? "ERROR: could not find the SVG string nor file.\n" : '';
			}
		}
	}
	
	//$svg_content_string = preg_replace("/(<.*?svg)([^>]?)/si", '\',$svg_content_string);
	
	$pos_svg = mb_strpos($svg_content_string, 'svg');
	$svg_content_string=mb_substr($svg_content_string,0,$pos_svg+3) . $namespaces . mb_substr($svg_content_string,$pos_svg+3);
	
	if ($TRANSLALTION == 1) {
		translation_fig_svg($left_panel_width, $svg_content_string, $question_info, $question_fragment_id, $question_fragment_imagefile);
	}
	else {
		//$svg_string, $width, $x_offset, $y_offset
		$x_offset = $pdf->getX();
		$y_offset = $pdf->getY();
		plain_fig_svg($svg_content_string, $left_panel_width, $x_offset, $y_offset, $question_fragment_imagefile);
		//$png_file = SvgStringToPng($svg_content_string);
		//place_png_onDRAFT(166, $png_file);
	}
}

function exam_answerlist ($answerlist_xml, $question_info) {
	global $verboseXML;
	global $pdf;
	global $left_panel_width;
	global $right_panel_width;
	global $answersplit_width;
	global $left_panel_list_width;
	global $TRANSLALTION;
	
	echo ($verboseXML > 1) ? "  " . $answerlist_xml->getName() . ":\n" : '';
	
	//TODO start answers
	$a_list = $answerlist_xml->children();
	foreach ($a_list as $a_element) {
		$a_element_name = $a_element->getName();
		switch ($a_element_name) {
			case 'answersplit':
				echo ($verboseXML > 1) ? "    " . $a_element_name . ": " . $a_element . "\n" : '';
				$question_fragment_id = $a_element['id'];
				$text = $a_element->asXML();
				$text = preg_replace(':.+?\>(.+)</.+:','$1',$text); // strip preciding and trailing xml tags from html content
				$html = tex_to_html($text);
				if ($TRANSLALTION == 1) {
					translation_box($answersplit_width, $text, $html, $question_info, $question_fragment_id);
				}
				else {/*
					$html = '<ul><li>' . $html . '</li></ul>';
					$pdf->writeHTMLLeft($html);
					//$pdf->writeHTML($html);
					$pdf->Ln(1);*/
				}
				break;
			case 'choice':
				echo ($verboseXML > 1) ? "    " . $a_element_name . ": " . $a_element . "\n" : '';
				$question_fragment_id = $a_element['id'];
				$text = $a_element->asXML();
				$text = preg_replace(':.+?\>(.+)</.+:','$1',$text); // strip preciding and trailing xml tags from html content
				$html = tex_to_html($text);
				if ($TRANSLALTION == 1) {
					translation_box($left_panel_list_width, $text, $html, $question_info, $question_fragment_id);
				}
				else {
					$html = '<ul><li>' . $html . '</li></ul>';
					$pdf->writeHTMLLeft($html);
					//$pdf->writeHTML($html);
					$pdf->Ln(1);
				}
				break;
			default:
				echo ($verboseXML > 0) ? "Undefined answerlist element:" . $l_element_name . ".\n" : '';
		}
	}
}

function exam_comment ($comment_xml, $question_info) {
    global $verboseXML;
    global $pdf;
    global $left_panel_width;
    global $right_panel_width;
    global $TRANSLALTION;

    $question_fragment_id = $comment_xml['id'];

    echo ($verboseXML > 1) ? "  " . $comment_xml->getName() . ": " . $comment_xml . "\n" : '';
    
    $text = $comment_xml;
    $html = base64_decode($text);
    $pdf->writeHTML($html);
    
    /*
    $text = $comment_xml->asXML();
    $text = preg_replace(':.+?\>(.+)</.+:s','$1',$text); // strip preciding and trailing xml tags from html content
    if ($text != '<comment/>') {
		//echo 'comment base: ' . $text . "\n";
		//$html = '$text is empty';
		$html = base64_decode($text);
		//echo 'comment html: ' . $html . "\n";

		if ($TRANSLALTION == 1) {
			$pdf->writeHTML($html);
			$pdf->Ln(1);
		}
	}*/
}

function translation_box_old ($width, $text, $html, $question_info, $question_fragment_id) {
	global $pdf;
	global $verboseTranslationBox;
	global $left_panel_width;
	global $left_panel_multiplier;
	global $left_panel_list_width;
	global $left_panel_list_multiplier;
	global $right_panel_width;
	global $right_panel_multiplier;
	global $answersplit_width;
	global $answersplit_multiplier;
	global $TEST_COLOR;
	
	$startpoint_x = $pdf->getX();
	$startpoint_y = $pdf->getY();
	$startpoint_page_number = $pdf->getPage();
	
	$content = $question_info['id'] . "-" . $question_info['info'] . "-" . $question_fragment_id;
	
	switch ($width) {
		case $left_panel_width     : $multiplier = $left_panel_multiplier     ; break;
		case $right_panel_width    : $multiplier = $right_panel_multiplier    ; break;
		case $answersplit_width    : $multiplier = $answersplit_multiplier    ; break;
		case $left_panel_list_width: $multiplier = $left_panel_list_multiplier; break;
		default: echo "Could not define a multiplier value. This is bad. Fix it!";
	}
	
	echo ($verboseTranslationBox > 1) ? "       " . $multiplier . "\n" : '';
	
	$height = strlen($text)*$multiplier;
	$height = floor($height*10)/10;
	
	$html_height = getheight_writeHTMLLeft($html);
	
	/*
	// test if the Text and the HandwritingScanBox fits onto this page. add newpage and go to the coordinates from old page, test if it fits, if yes remove the test page and print to original page 
	$pdf->addPage();//dont write on a page in the final document. This page will be deleted after the test
	$pdf->setX($startpoint_x);
	$pdf->setY($startpoint_y);
	
	$teststart_page_number = $pdf->PageNo();
	
	$html_test = "<font color=\"$TEST_COLOR\">" . $html . "</font>"; // for debuging üurpose only. This WILL mess with your mind if you see it ... "#FFFFFF" makes it white
	$pdf->writeHTMLLeft($html);
	//$pdf->writeHTML($html_test);
	$pdf->Ln(1);
	$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
	$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
	$rectangle["width"]    = $width;
	$rectangle["height"]   = $height;
	$pdf->HandwritingScanBox(	$rectangle["x_offset"],
								$rectangle["y_offset"],
								$rectangle["width"],
								$rectangle["height"],
								$content,
								1 ); // $visibility: 1=visible, 0=invisible
	
	// check if the white stuff made a pagebreak and handle it
	$pdf->writeHTML('<font color="white"></font>');//write a nonbreakable whitespace
	$testend_page_number = $pdf->PageNo();
	
	// remove test sites again
	$temp_nowpage = $testend_page_number;
	while ( $startpoint_page_number < $temp_nowpage) {
		$pdf->deletePage($temp_nowpage);
		$pdf->lastPage();
		$temp_nowpage = $pdf->getPage();
	}
	*/
	
	//calculate height for tests with rectangles
	$height = floor($height*10)/10;
	
	$pdf_page_heigth = $pdf->getPageHeight();// get page height in user units
	$text_height = $pdf_page_heigth - $pdf_bottom_margin - $pdf_top_margin;
	$y_max = $pdf_page_heigth - $startpoint_y - $pdf_bottom_margin;
	
	$y_after_text = $startpoint_y + $html_height;
	$y_after_box  = $startpoint_y + $html_height + $height;
	
	
	////  newtry start
	if ( $y_max < $y_after_box ) { //
		if ($text_height < $html_height + $height) { // fig and translation fig DO NOT FIT on the same page
			$pdf->writeHTMLLeft($html);
			//$pdf->writeHTML($html);
			$pdf->AddPageIBO();
		} else { // fig and translation fig DO FIT on the same page
			$pdf->AddPageIBO();
			$pdf->writeHTMLLeft($html);
			//$pdf->writeHTML($html);
		}
			$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
			$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
			$rectangle["width"]    = $width;
			$rectangle["height"]   = $text_height;
			$pdf->HandwritingScanBox(	$rectangle["x_offset"],
										$rectangle["y_offset"],
										$rectangle["width"],
										$rectangle["height"],
										$content,
										1 ); // $visibility: 1=visible, 0=invisible
	}
	else { // fits on page
		$pdf->writeHTMLLeft($html);
		//$pdf->writeHTML($html);
		$pdf->Ln(1);
		$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
		$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
		$rectangle["width"]    = $width;
		$rectangle["height"]   = $height;
		$pdf->HandwritingScanBox(	$rectangle["x_offset"],
									$rectangle["y_offset"],
									$rectangle["width"],
									$rectangle["height"],
									$content,
									1 ); // $visibility: 1=visible, 0=invisible
	}
	////  newtry end
	
	/*
	if ($y_after_box >= $y_max ) {
		$pdf->addPage();
		$height = $text_height - 1;
	}

	if ( $testend_page_number == $teststart_page_number) { // reset page number, x and y insert point to page origin since we came back to the start page
		global $pdf_left_margin;
		global $pdf_top_margin;
		
		// return to startpoint and remove testpage
		$pdf->setPage($startpoint_page_number);
		$pdf->setX($startpoint_x);
		$pdf->setY($startpoint_y);
		
		// write the text and HandwritingScanBox to the PDF
		echo "$html \n";
		$pdf->writeHTMLLeft($html);
		//$pdf->writeHTML($html);
		$pdf->Ln(1);
		$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
		$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
		$rectangle["width"]    = $width;
		$rectangle["height"]   = $height;
		$pdf->HandwritingScanBox(	$rectangle["x_offset"],
									$rectangle["y_offset"],
									$rectangle["width"],
									$rectangle["height"],
									$content,
									1 ); // $visibility: 1=visible, 0=invisible
	} 
	else { // test if the Text and the HandwritingScanBox fits onto one page. add newpage, test if it fits, if yes remove the test page and print to original page 
		$pdf->addPage();//dont write on a page in the final document. This page will be deleted after the test
		$teststart_page_number = $pdf->PageNo();
	
		$pdf->writeHTML($html);
		$pdf->Ln(1);
		$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
		$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
		$rectangle["width"]    = $width;
		$rectangle["height"]   = $height;
		$pdf->HandwritingScanBox(	$rectangle["x_offset"],
									$rectangle["y_offset"],
									$rectangle["width"],
									$rectangle["height"],
									$content,
									1 ); // $visibility: 1=visible, 0=invisible
	
		// check if the white stuff made a pagebreak and handle it
		$pdf->writeHTML('<font color="white"></font>');//write a nonbreakable whitespace
		$testend_page_number = $pdf->PageNo();
		
		if ( $testend_page_number > $teststart_page_number) { // reset page number, x and y insert point to page origin since we came back to the start page
			// remove test sites again
			$temp_nowpage = $testend_page_number;
			while ( $startpoint_page_number < $temp_nowpage) {
				$pdf->deletePage($temp_nowpage);
				$pdf->lastPage();
				$temp_nowpage = $pdf->getPage();
			}
			
			// return to startpoint on startpage
			$pdf->setPage($startpoint_page_number);
			$pdf->setX($startpoint_x);
			$pdf->setY($startpoint_y);
			
			// print html normally on multiplepages
			$pdf->writeHTML($html);
			$pdf->Ln(1);
			
			//check if translation box fits to the current page, if not, add newpage and make translationbox as bis as possible
			$current_y = $pdf->getY();
			global $pdf_bottom_margin;
			global $pdf_top_margin;
			$pdf_page_heigth = $pdf->getPageHeight();// get page height in user units
			$text_height = $pdf_page_heigth - $pdf_bottom_margin - $pdf_top_margin;
			$y_max = $pdf_page_heigth - $current_y - $pdf_bottom_margin;
			$y_after_box = $current_y + $height;
			if ($y_after_box >= $y_max ) {
				$pdf->addPage();
				$height = $text_height - 1;
			}
			
			// print translation box 
			$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
			$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
			$rectangle["width"]    = $width;
			$rectangle["height"]   = $height;
			$pdf->HandwritingScanBox(	$rectangle["x_offset"],
										$rectangle["y_offset"],
										$rectangle["width"],
										$rectangle["height"],
										$content,
										1 ); // $visibility: 1=visible, 0=invisible
			
			if ($y_after_box >= $y_max ) {
				$pdf->addPage();
			}
		}
		else {
			// it fits, dont have to do anything
		}
	}
	*/
}

function translation_box ($width, $text, $html, $question_info, $question_fragment_id) {
	global $pdf;
	global $verboseTranslationBox;
	global $left_panel_width;
	global $left_panel_multiplier;
	global $left_panel_list_width;
	global $left_panel_list_multiplier;
	global $right_panel_width;
	global $right_panel_multiplier;
	global $answersplit_width;
	global $answersplit_multiplier;
	global $TEST_COLOR;
	global $pdf_left_margin;
    global $pdf_top_margin;
    global $pdf_bottom_margin;

	
	$startpoint_x = $pdf->getX();
	$startpoint_y = $pdf->getY();
	$startpoint_page_number = $pdf->getPage();
	
	$content = $question_info['id'] . "-" . $question_info['info'] . "-" . $question_fragment_id;
	
	switch ($width) {
		case $left_panel_width     : $multiplier = $left_panel_multiplier     ; break;
		case $right_panel_width    : $multiplier = $right_panel_multiplier    ; break;
		case $answersplit_width    : $multiplier = $answersplit_multiplier    ; break;
		case $left_panel_list_width: $multiplier = $left_panel_list_multiplier; break;
		default: echo "Could not define a multiplier value. This is bad. Fix it!";
	}
	
	echo ($verboseTranslationBox > 1) ? "       " . $multiplier . "\n" : '';
	
	$height = strlen($text)*$multiplier;
	$height = floor($height*10)/10;
	$html_height = getheight_writeHTMLLeft($html);
	$pdf_page_heigth = $pdf->getPageHeight();// get page height in user units
	$textheight      = $pdf_page_heigth - ($pdf_bottom_margin + $pdf_top_margin);
	$y_max           = $pdf_page_heigth - $pdf_bottom_margin;
	// do that one better...
	$y_after_text    = $startpoint_y + $html_height + 5;
	$y_after_box     = $startpoint_y + $html_height + $height + 10;
	
	print "html_height:$html_height\nheight:$height\nstart: $startpoint_y\n";
	
	////  newtry start
	if ( $y_max < $y_after_box ) { // not everything fits on the current page
		if ($textheight < $html_height + $height + 10) { // text and translation DO NOT FIT on the same page
			if ( $y_after_text < $y_max ) { // text fits on the current page
				print "text fits on the current page\n";
				$pdf->writeHTMLLeft($html);
				//$pdf->writeHTML($html);
				$pdf->AddPageIBO();
			} 
			else { // text does not fit on the current page
				print "text does not fit on the current page\n";
				$pdf->AddPageIBO();
				$pdf->writeHTMLLeft($html);
				$pdf->AddPageIBO();
			}
		} else { // fig and translation fig DO FIT on the same page
			print "text and translation fig DO FIT on the same page\n";
			$pdf->AddPageIBO();
			$pdf->writeHTMLLeft($html);
			//$pdf->writeHTML($html);
			$pdf->Ln(1);

		}
		
		if ( $height > $textheight ) {
			$height = $textheight;
		}
		
		$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
		$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
		$rectangle["width"]    = $width;
		$rectangle["height"]   = $height;
		$pdf->HandwritingScanBox(	$rectangle["x_offset"],
									$rectangle["y_offset"],
									$rectangle["width"],
									$rectangle["height"],
									$content,
									1 ); // $visibility: 1=visible, 0=invisible
		$pdf->Ln(1);
	}
	else { // text and translationbox fit on current page
		print "text and translation fits on current page\n";
		$pdf->writeHTMLLeft($html);
		//$pdf->writeHTML($html);
		$pdf->Ln(1);
		$rectangle["x_offset"] = $pdf->getX(); // current $x coordinate
		$rectangle["y_offset"] = $pdf->getY(); // current $y coordinate
		$rectangle["width"]    = $width;
		$rectangle["height"]   = $height;
		$pdf->HandwritingScanBox(	$rectangle["x_offset"],
									$rectangle["y_offset"],
									$rectangle["width"],
									$rectangle["height"],
									$content,
									1 ); // $visibility: 1=visible, 0=invisible
		$pdf->Ln(1);
	}
}

/* no tables!!!
function translation_table ($width, $html, $question_info) {
	global $pdf;
	global $verboseTranslationTable;
	global $left_panel_width;
	global $right_panel_width;
	
	$startpoint_x = $pdf->getX();
	$startpoint_y = $pdf->getY();
	$startpoint_page_number = $pdf->PageNo();
	
	$content = $question_info['id'] . "-" . $question_info['info'] . "-" . $question_fragment_id;
	
	//$pdf->SetFillColor(255);
	$pdf->SetColor(255);
	$pdf->SetTextColor(255);
	$pdf->SetDrawColor(255, 255, 255);
	$pdf->SetLineWidth(0);

	//$html_translate = str_replace('%TABLE_FONT_COLOR%', 'white', $html);
	//$html_white = str_replace('%TABLE_BORDER_COLOR%', 'white', $html_translate);
		
	$pdf->writeHTML($html);
	$pdf->writeHTML($html);
	
	// check for pagebreak
	$endpoint_page_number = $pdf->PageNo();
	if ( $endpoint_page_number != $startpoint_page_number) { // reset x and y insert point to page origin since we are on a newpage now
		global $pdf_left_margin;
		global $pdf_top_margin;
		$pdf->setX($pdf_left_margin);
		$pdf->setY($pdf_top_margin);
	} else { // reset x and y values to those before the test
		$pdf->setX($startpoint_x);
		$pdf->setY($startpoint_y);
	}
	
	// write the visible text and HandwritingScanBox to the PDF
	$pdf->SetLineWidth(.3);
	$pdf->SetDrawColor(0);
	$pdf->SetTextColor(0);
	//$pdf->writeHTML($html);
	$pdf->SetTextColor(255);
	//$pdf->writeHTML($html_translate);
}*/

function translation_fig_svg ($width, $svg_string, $question_info, $question_fragment_id) {
	global $pdf;
	global $verboseTranslationFig;
	global $left_panel_width;
	global $right_panel_width;
	global $pdf_left_margin;
    global $pdf_top_margin;
    global $pdf_bottom_margin;
	
	#print $svg_string;
	// this drives me crazy:
	$translation_svgimg = preg_replace('/<.*?text id\=\"IBOtranslation.+?<\/.*?text\>/','', $svg_string);
	
	//The following regex generates a "Segmentation fault: 11" with some graphics
	//$translation_svgimg = preg_replace('/<([^>]*?)text((?!text>).)+?id="IBOtranslation.+?<\/\1text>/si', '', $svg_string);
	// just checking:
	#die("replaced\n:$translation_svgimg:\n");
	#print "replaced\n:$translation_svgimg:\n";
	
	if ($translation_svgimg == $svg_string) {
		$info_text_no_translation = "This figure does not require any translation.";
		print $info_text_no_translation;
		$x_offset = $pdf->getX();
		$y_offset = $pdf->getY();
		plain_fig_svg($svg_string, $width, $x_offset, $y_offset);
		return;
	}
	
	$startpoint_x = $pdf->getX();
	$startpoint_y = $pdf->getY();
	$startpoint_page_number = $pdf->PageNo();
	
	$content = $question_info['id'] . "-" . $question_info['info'] . "-" . $question_fragment_id;
	
	$style_invisible = array('width' => 0, 'cap' => 'butt', 'join' => 'miter', 'dash' => 0, 'color' => array(255, 255, 255));
	
	list ($original_width, $original_height) = get_SVG_ratio_from_string($svg_string);
	echo ($verboseTranslationFig > 1) ? "$original_width,$original_height\n" : '';
	
	//calculate height for tests with rectangles
	$height = $width * ($original_height / $original_width);
	$height = floor($height*10)/10;
	
	$pdf_page_heigth = $pdf->getPageHeight();// get page height in user units
	
	$y_max        = $pdf_page_heigth -  $pdf_bottom_margin ;
	$max_y_height = $pdf_page_heigth - ($pdf_bottom_margin + $startpoint_y  ) ;
	$text_height  = $pdf_page_heigth - ($pdf_bottom_margin + $pdf_top_margin) ;
	$y_after_fig  = $startpoint_y + $height + 5 ;
	$y_after_box  = $startpoint_y + $height + $height + 10 ;
	
	if ( $y_max < $y_after_box ) { // not everything fits on the current page
		if ($text_height < $height + $height + 10) { // fig and translation fig DO NOT FIT on the same page
			if ( $y_after_fig < $y_max ) { // figure fits on the current page
				$x_offset = $pdf->getX();
				$y_offset = $pdf->getY();
				plain_fig_svg($svg_string, $width, $x_offset, $y_offset, $question_fragment_imagefile);
				$pdf->AddPageIBO();
			}
		} else { // fig and translation fig DO FIT on the same page
			$pdf->AddPageIBO();
			$x_offset = $pdf_left_margin;
			$y_offset = $pdf_top_margin;
			plain_fig_svg($svg_string, $width, $x_offset, $y_offset, $question_fragment_imagefile);
		}
	}
	else { // everything fits on the current page
		$x_offset = $pdf->getX(); // current $x coordinate
		$y_offset = $pdf->getY(); // current $y coordinate
		$PNG = SvgStringToPng($svg_string, $question_fragment_imagefile);
		$pdf->Image($file=$PNG, $x=$x_offset, $y=$y_offset, $w=$width, $h='', $link='', $align='', $palign='', $border=0, $fitonpage=false);
		$pdf->setX($pdf->getImageRBX());
		$pdf->setY($pdf->getImageRBY());
		$pdf->Ln(1);
	}
	
	if ( $height > $text_height ) {
		$height = $text_height;
	}
	
	$x_offset = $pdf->getX(); // current $x coordinate
	$y_offset = $pdf->getY(); // current $y coordinate
	$PNG = SvgStringToPng($translation_svgimg, $question_fragment_imagefile);
	$pdf->Image($file=$PNG, $x=$x_offset, $y=$y_offset, $w=$width, $h='', $link='', $align='', $palign='', $border=0, $fitonpage=false);
	$pdf->HandwritingScanBox(	$x_offset,
								$y_offset,
								$width,
								$height,
								$content,
								1 ); // $visibility: 1=visible, 0=invisible
}

function plain_fig_svg($svg_string, $width, $x_offset, $y_offset, $question_fragment_imagefile) {
	global $pdf;
	global $verboseTranslationFig;
	global $left_panel_width;
	global $right_panel_width;
	global $pdf_bottom_margin;
	global $pdf_top_margin;
	
	$startpoint_page_number = $pdf->PageNo();
	
	list ($original_width, $original_height) = get_SVG_ratio_from_string($svg_string);
	
	echo ($verboseTranslationFig > 1) ? "$original_width,$original_height\n" : '';
	
	//echo "ow:$original_width, oh:$original_height\n";
	
	//calculate height for tests with rectangles
	$height = $width * ($original_height / $original_width);
	$height = floor($height*10)/10;
	
	$pdf_page_heigth = $pdf->getPageHeight();// get page height in user units
	$text_height = $pdf_page_heigth - $pdf_bottom_margin - $pdf_top_margin;
	$y_max = $pdf_page_heigth - $pdf_bottom_margin;
	print "$y_offset + $height\n";
	$y_after_box = $y_offset + $height;
	if ($y_after_box >= $y_max ) {
		$pdf->AddPageIBO();
		print "page added: Y=$y_after_box\n";
	}
	
	// print image the PDF
	$PNG = SvgStringToPng($svg_string, $question_fragment_imagefile);
	$pdf->Image($file=$PNG, $x=$x_offset, $y=$y_offset, $w=$width, $h='', $link='', $align='', $palign='', $border=0, $fitonpage=false);
	$pdf->setX($pdf->getImageRBX());
	$pdf->setY($pdf->getImageRBY());
	$pdf->Ln(1);
}

/*
function place_png_onDRAFT ($width, $PNG) {
	global $pdf;
	global $verboseTranslationFig;
	global $left_panel_width;
	global $right_panel_width;
	pdf_bottom_margin
	pdf_top_margin
	height
	
	
	$startpoint_x = $pdf->getX();
	$startpoint_y = $pdf->getY();
	$startpoint_page_number = $pdf->PageNo();
	
	$pdf_page_heigth = $pdf->getPageHeight();// get page height in user units
	$text_height = $pdf_page_heigth - $pdf_bottom_margin - $pdf_top_margin;
	$y_max = $pdf_page_heigth - $startpoint_y - $pdf_bottom_margin;
	
	$y_after_box = $startpoint_y + $height;
	if ($y_after_box >= $y_max ) {
		$pdf->AddPageIBO();
		$height = $text_height - 1;
	}
	
	// print image the PDF
	$x_offset = $pdf->getX(); // current $x coordinate
	$y_offset = $pdf->getY(); // current $y coordinate
	$pdf->Image($file=$PNG, $x=$x_offset, $y=$y_offset, $w=$width, $h='', $link='', $align='', $palign='', $border=0, $fitonpage=false);
	$pdf->setX($pdf->getImageRBX());
	$pdf->setY($pdf->getImageRBY());
	$pdf->Ln(1);
}
*/

# returns /path/to/png_file.png
function SvgStringToPng ($svg_string, $question_fragment_imagefile) {
	global $FILES_TO_UNLINK_UPON_SUCCESSFUL_COMPLETION;
	global $verboseSVGtoPNG;
	
	//print "SvgStringToPng:\n$svg_string";
	
	$tmpfname_svg = tempnam ( './temporarySVGs' , 'mysvgs_' );// tempfile: read/write permissions
	rename($tmpfname_svg, $tmpfname_svg .= '.svg');
	
	if (is_writable($tmpfname_svg)) {
		if (!$handle = fopen($tmpfname_svg, "a")) {
			 die( "Can not open file $tmpfname_svg" );
		}
		// writing $svg_string to temporary file
		if (!fwrite($handle, $svg_string)) {
			die( "Can not write to file $tmpfname_svg" );
			print ( "Can not write to file $tmpfname_svg" );
		}
		fclose($handle);
	} else {
		die( "Temporary file is not writable $tmpfname_svg" );
	}
	
	$tmpfname_png = tempnam ( './temporaryPNGs' , 'mypngs_' );// tempfile: read/write permissions
	rename($tmpfname_png, $tmpfname_png .= '.png');
	
	$outval = system("inkscape --export-width=2245 --export-background=white --export-png=$tmpfname_png $tmpfname_svg", $retval);# &> /dev/null could be nice, but might mess up check for created bitmap
	// print "\naut $retval tuo\nrv $outval vr\n";
	if ( strstr($outval, 'Bitmap saved as: ') ) {
		echo ($verboseSVGtoPNG > 1) ? "Successfully created bitmap. Deleting temporary svg file: $tmpfname_svg\n" : '';
		if (!unlink($tmpfname_svg)) { // deletes file
			print "ERROR: could not delete temporary svg.\n";
		}
	}
	else {
		print "ERROR: could not create bitmap.";
	}
	
	array_push($FILES_TO_UNLINK_UPON_SUCCESSFUL_COMPLETION, $tmpfname_png);
	
	return $tmpfname_png;
}

function get_SVG_ratio($file) {
	global $pdf;
	
	if (($svgimg = file_get_contents($file)) && preg_match('/<[^\>]*?svg([^\>]*)>/si', $svgimg, $regs)) {
		$svgtag = $regs[1];
		if (preg_match('/[\s]+width[\s]*=[\s]*"([^"]*)"/si', $svgtag, $w) && preg_match('/[\s]+height[\s]*=[\s]*"([^"]*)"/si', $svgtag, $h))
		return array($w[1], $h[1]);
	} else {
		echo ($verboseTranslationFig > 0) ? "ERROR: SVG figure not found. $file" : '';
	}
}

function get_SVG_ratio_from_string ($svg_string) {
	global $verboseTranslationFig;
	
	if (preg_match('/<[^>]*?svg([^>]*)>/si', $svg_string, $regs) ) {
		$svgtag = $regs[1];
		if (preg_match('/[\s]+width[\s]*=[\s]*"([^"]*)"/si', $svgtag, $w) && preg_match('/[\s]+height[\s]*=[\s]*"([^"]*)"/si', $svgtag, $h)) {
			return array($w[1], $h[1]);
		}
		else {
			echo ($verboseTranslationFig > 0) ? "ERROR: could not extract widht or height from SVG string." : '';
		}
	}
	else {
		echo ($verboseTranslationFig > 0) ? "ERROR: could not extract attributes from SVG string." : '';
	}
}

function tex_to_html ($text) {
	$html = preg_replace('/\[(\/?(sub|sup|b|i))\]/','<\1>',$text);
	return $html;
}

function getheight_writeHTML ($html) {
	global $pdf;
	global $pdf_top_margin;
	global $pdf_top_margin;
	
	// store current object
	$pdf->startTransaction();
	// store starting values
	$start_y = $pdf->GetY();
	$start_page = $pdf->getPage();
	// call your printing functions with your parameters
	$pdf->writeHTML($html);
	// get the new Y

	$end_y = $pdf->GetY();
	$end_page = $pdf->getPage();
	// calculate height
	$height = 0;
	
	if ($end_page == $start_page) {
		$height = $end_y - $start_y;
	}
	else {
		for ($page=$start_page; $page <= $end_page; ++$page) {
			$pdf->setPage($page);
			if ($page == $start_page) {
				// first page
				$height = $pdf->getPageHeight() - $start_y - $pdf_bottom_margin;
			} elseif ($page == $end_page) {
				// last page
				$height = $end_y - $pdf_top_margin;
			} else {
				$height = $pdf->getPageHeight() - $pdf_top_margin - $pdf_bottom_margin;
			}
		}
	}
	
	//print $height;
	
	// restore previous object 
	$pdf = $pdf->rollbackTransaction();
	return $height;
}

function getheight_writeHTMLLeft ($html) {
	global $pdf;
	global $pdf_top_margin;
	global $pdf_top_margin;
	
	// store current object
	$pdf->startTransaction();
	// store starting values
	$start_y = $pdf->GetY();
	$start_page = $pdf->getPage();
	// call your printing functions with your parameters
	$pdf->writeHTMLLeft($html);
	// get the new Y

	$end_y = $pdf->GetY();
	$end_page = $pdf->getPage();
	// calculate height
	$height = 0;
	
	if ($end_page == $start_page) {
		$height = $end_y - $start_y;
	}
	else {
		for ($page=$start_page; $page <= $end_page; ++$page) {
			$pdf->setPage($page);
			if ($page == $start_page) {
				// first page
				$height = $pdf->getPageHeight() - $start_y - $pdf_bottom_margin;
			} elseif ($page == $end_page) {
				// last page
				$height = $end_y - $pdf_top_margin;
			} else {
				$height = $pdf->getPageHeight() - $pdf_top_margin - $pdf_bottom_margin;
			}
		}
	}
	
	//print $height;
	
	// restore previous object 
	$pdf = $pdf->rollbackTransaction();
	return $height;
}

function getheight_figure ($html) {
	global $pdf;
	global $pdf_top_margin;
	global $pdf_top_margin;
	
	// store current object
	$pdf->startTransaction();
	// store starting values
	$start_y = $pdf->GetY();
	$start_page = $pdf->getPage();
	// call your printing functions with your parameters
	$pdf->writeHTMLLeft($html);
	// get the new Y

	$end_y = $pdf->GetY();
	$end_page = $pdf->getPage();
	// calculate height
	$height = 0;
	
	if ($end_page == $start_page) {
		$height = $end_y - $start_y;
	}
	else {
		for ($page=$start_page; $page <= $end_page; ++$page) {
			$pdf->setPage($page);
			if ($page == $start_page) {
				// first page
				$height = $pdf->getPageHeight() - $start_y - $pdf_bottom_margin;
			} elseif ($page == $end_page) {
				// last page
				$height = $end_y - $pdf_top_margin;
			} else {
				$height = $pdf->getPageHeight() - $pdf_top_margin - $pdf_bottom_margin;
			}
		}
	}
	
	//print $height;
	
	// restore previous object 
	$pdf = $pdf->rollbackTransaction();
	return $height;
}


?>

