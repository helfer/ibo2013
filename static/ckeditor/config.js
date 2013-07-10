/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	config.forcePasteAsPlainText = true;
	config.toolbar = [
    [ 'Bold', 'Italic', 'Subscript', 'Superscript' ]
	];
	config.removePlugins = 'elementspath';
	config.resize_enabled = false;
	config.extraPlugins = 'autogrow';
	config.autoGrow_minHeight = 94;
	config.autoGrow_maxHeight = 0;
	config.autoGrow_onStartup = true;
	config.width = '90%';
	config.resize_maxWidth = 750;
};


