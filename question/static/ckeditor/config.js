/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	config.forcePasteAsPlainText = true;
	config.toolbar = [
    [ 'Bold', 'Italic', 'Subscript', 'Superscript','-','BidiLtr','BidiRtl' ]
	];
	config.toolbarLocation = 'bottom';
	config.removePlugins = 'elementspath';
	config.resize_enabled = false;
	config.extraPlugins = 'autogrow,bidi';
	config.autoGrow_minHeight = 0;
	config.autoGrow_maxHeight = 0;
	config.autoGrow_onStartup = true;
	config.width = '100%';
	config.resize_maxWidth = 750;
	config.htmlEncodeOutput = false;
    config.entities = false;
	config.disableNativeSpellChecker = false;
};


