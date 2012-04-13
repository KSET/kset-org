// -----------------------------------------------------------------------------------
//
//	Lightbox v2.05
//	by Lokesh Dhakar - http://www.lokeshdhakar.com
//	Last Modification: 3/18/2011
//	Last TwoHawks (HTH) Modification: 10/13/2011
//
//	For more information, visit:
//	http://lokeshdhakar.com/projects/lightbox2/
//	
//	Modification by Fabian Lange - blog.hma-info.de
//	 - Integration of automatic resize from Michael R. Bagnall - elusivemind.net & Sebastien Grosjean - ZenCocoon.com
//     http://seb.box.re/2006/11/22/lightbox-2-auto-resizing-enhancement
//     http://blog.hma-info.de/2008/04/09/latest-lightbox-v2-with-automatic-resizing/
//     (Search for "SEB" for code)
//	 - do not display caption of previous image if new image has none
//	 - moved so-called opera "hack" to resolve disortion in FireFox (redone/corrected in TwoHawks (HTH) version)
//	 - readded window sizes to getPageSize() -part of automatic resize feature
//
//	Licensed under the Creative Commons Attribution 2.5 License - http://creativecommons.org/licenses/by/2.5/
//  	- Free for use in both personal and commercial projects
//		- Attribution requires leaving author name, author link, and the license info intact.
//	
//  Thanks: Scott Upton(uptonic.com), Peter-Paul Koch(quirksmode.com), and Thomas Fuchs(mir.aculo.us) for ideas, libs, and snippets.
//  		Artemy Tregubenko (arty.name) for cleanup and help in updating to latest ver of proto-aculous.
//
// ############################################
// TwoHawks/HTH Modifications (Search for "HTH" for code)  
//                                         {Internal ref: dev file = scrlightboxHTHcustCap2a.js / stylightboxHTHcustCap2a.css}
//
/* VERSION: LB2.05 WITH SEB AUTORESIZE MOD AND HTH RECAPTIONING VERSION 2A MOD:
   ----- FEATURES -------------------------------------------------------------------------------
   - SEB AutoResize (with tweaks and fixes)
   - Bottom Prev/Next Nav Buttons Added
   - Close Button Relocated Up under Image (v2a) {v2b is 2a, but has the Close Button on Bottom }
   - Caption Enhancements:
       - Independently managed Title, Description, and misc sections
       - Extra Attributes for facilitating easier application of enhancements (formatting, links, scripts) to titles and/or descriptions and/or Image '# of #' sections
       - Easy to add persistent links, or even new sections (your own new attributes) for adding more complexity to the caption area (if you feel ok handling a little code, that is)
   - minor fixes and adjustments
   - ++misc: see list below for details
*/
/*  To Lokesh, Fabian, and Sebastian: if you find any of my proposed changes worthy of inclusion in your LB updates, by all means feel free to incorporate.
in gratitude, TwoHawks
*/
//   ----- HTH MODS CHANGES HISTORY  -------------------------------------------------------
//  NOTE:  lightbox.js and lightbox.css both changed (content, names, relative locations...)
//            -- my files are named differently due to the way I manage files. Adjust accordingly.
//            I use a custom reset-styles-base. This has not yet been tested in a non-reset-styles-base environ = use at your own risk 
//            This js file is comment heavy. You can lose some weight by deleting all TwoHawks comments after learning from them
//            You must keep the comments above the Hashes (lines1-25) and do well to also leave in at least up to line 31
//

/* HTH Version 2a mods    TwoHawks NewCap:  Captions redo workup
 - created more individuated sections for capton title, title-anchor option, and description option, including moving the close button (made things easier for various technical reasons). 
 - Caveat: still need to write code for predetermining caption height (one day maybe). For now I have two places where I make some slight hard-wired  adjustments for doing 'well enough'
 - While I do not yet use the experimental html5 doctype, I am implementing the new data-xxxx attributes

 YOU ARE BEST OFF DOING A DIFF COMPARE with the original and/or with HTH version 1b to observe the changes, but they are well documented throughout
 For this particular mod, look for occurances of "HTH NewCap"
*/

/*    #### HTH Version 1b mods  #### 
    - close button relocated UP ..just below image
*/
/*    #### HTH Version 1a mods  #### 
    - added Bottom Navigation Buttons
    - fixed a number of problems with SEB overlay not expanding for window resizing
        or in certain browsers going full width and/or height. (unconventional arrayPageSize tweaks included - watch for those)
    - added number of tiny edits to SEB for postitioning to accomodate bottom button nav
    - added conditional "Get Full Size" link when images resized down (displays when images display sized down)
    - minor number caption issue (in HTH mod) corrected 
    - show/hide for added objects addresses an IE  issue when applying positioning to certain LB elements that I added
*/
/*    #### HTH Version ALL MODS  #### 
    - fixed problem with Close Button 'Anchor' being offset downward by font-size applied to outerImageContainer when using 'em's for font management in base site css (as many of us do)
    - added some Opera fixes for: "overlay height will not work on sites using html height:100%; base css" problem
    - reverted original Opera so-called "hack" adjustment back to original location, modifying code so it now works correctly with all, and without intereference with other, browsers and/or mods
*/

/*    #### REMAINING ISSUES (TwoHawks Notes)  #### 
    - FIXED (but testing alternate fix): prev/next overlay does not resize when adjusting window size (ref: HTH SEB)
    - The Get Full Size" link uses a simple popup function I have included in the header.
    - Tested in Win FF2, 3.5-4.x, IE 6-8, Opera 9-11, Safari 3-X, Chrome X-X, 
    - Not Tested in IE9 or on Mac Browsers yet
*/
//
// Much Gratitude to Lokesh, and to everyone else for their contributions - THANK YOU!
// ----------------------------------------------------------------------------------------------
/*

    Table of Contents
    -----------------
    Configuration

    Lightbox Class Declaration
    - initialize()
    - updateImageList()
    - start()
    - changeImage()
    - adjustImageSize()
    - resizeImageContainer()
    - showImage()
    - updateDetails()
    - updateNav()
    - enableKeyboardNav()
    - disableKeyboardNav()
    - keyboardAction()
    - preloadNeighborImages()
    - getPageSize()
    - end()
    
    Function Calls
    - document.observe()
   
*/
// -----------------------------------------------------------------------------------

//
//  Configurationl
//
LightboxOptions = Object.extend({
    fileLoadingImage:        '/media/frontend/lightbox/images/loading.gif',     
    fileBottomNavCloseImage: '/media/frontend/lightbox/images/closelabel.gif',

    overlayOpacity: 0.8,   // controls transparency of shadow overlay

    animate: true,         // toggles resizing animations
    resizeSpeed: 10,        // controls the speed of the image resizing animations (1=slowest and 10=fastest)

    borderSize: 10,         //if you adjust the padding in the CSS, you will need to update this variable

//SEB1 Begin
    featBrowser: false,     // set it to true or false to choose to auto-adjust the maximum size to the browser
    breathingSize: 30,     // control the minimum space around the image box
//SEB1 End

//HTH Begin
    breathingSizeCaption: 50,   //HTH NewCap3 - you can add some px to compensate for caption height. 
                                //Suggest starting with 0, then see how it goes.
                                //50 is initially set here for the HTH Examples, where you can learn about this.
//HTH End

	// When grouping images this is used to write: Image # of #.
	// Change it for non-english localization
	labelImage: "Image",
	labelOf: "of"
}, window.LightboxOptions || {});

// -----------------------------------------------------------------------------------

var Lightbox = Class.create();

Lightbox.prototype = {
    imageArray: [],
    activeImage: undefined,
    
    // initialize()
    // Constructor runs on completion of the DOM loading. Calls updateImageList and then
    // the function inserts html at the bottom of the page which is used to display the shadow 
    // overlay and the image container.
    //
    initialize: function() {    
        
        this.updateImageList();
        
        this.keyboardAction = this.keyboardAction.bindAsEventListener(this);

        if (LightboxOptions.resizeSpeed > 10) LightboxOptions.resizeSpeed = 10;
        if (LightboxOptions.resizeSpeed < 1)  LightboxOptions.resizeSpeed = 1;

	    this.resizeDuration = LightboxOptions.animate ? ((11 - LightboxOptions.resizeSpeed) * 0.15) : 0;
	    this.overlayDuration = LightboxOptions.animate ? 0.2 : 0;  // shadow fade in/out duration

        // When Lightbox starts it will resize itself from 250 by 250 to the current image dimension.
        // If animations are turned off, it will be hidden as to prevent a flicker of a
        // white 250 by 250 box.
        var size = (LightboxOptions.animate ? 250 : 1) + 'px';
        

        // Code inserts html at the bottom of the page that looks similar to this:
        //
        //  <div id="overlay"></div>
        //  <div id="lightbox">
        //      <div id="outerImageContainer">
        //          <div id="imageContainer">
        //              <img id="lightboxImage">
        //              <div style="" id="hoverNav">
        //                  <a href="#" id="prevLink"></a>
        //                  <a href="#" id="nextLink"></a>
        //              </div>
        //              <div id="loading">
        //                  <a href="#" id="loadingLink">
        //                      <img src="images/loading.gif">
        //                  </a>
        //              </div>
        //          </div>
        //      </div>
        //      <div id="imageDataContainer">
        //          <div id="imageData">
        //              <div id="imageDetails">
//HTH NewCap1 new sections
        //                  <span id="bottomNav">
        //                     <a href="#" id="bottomNavClose">
        //                         <img src="images/closelabel.gif">
        //                     </a>
        //                 </span>
        //                  <span id="caption"></span>
        //                  <span id="numberDisplay"></span>
//HTH Bottom Nav1 Begin
        //                  <span id="hoverNav2">
        //                      <a href="#" id="prevLink2"></a>
        //                      <a href="#" id="nextLink2"></a>
	     //                   </span>								
//HTH Bottom Nav1 End
        //              </div>
        //          </div>
        //      </div>
        //  </div>


        var objBody = $$('body')[0];

		objBody.appendChild(Builder.node('div',{id:'overlay'}));
	
        objBody.appendChild(Builder.node('div',{id:'lightbox'}, [
            Builder.node('div',{id:'outerImageContainer'}, 
                Builder.node('div',{id:'imageContainer'}, [
                    Builder.node('img',{id:'lightboxImage'}), 
                    Builder.node('div',{id:'hoverNav'}, [
                        Builder.node('a',{id:'prevLink', href: '#' }),
                        Builder.node('a',{id:'nextLink', href: '#' })
                    ]),
                    Builder.node('div',{id:'loading'}, 
                        Builder.node('a',{id:'loadingLink', href: '#' }, 
                            Builder.node('img', {src: LightboxOptions.fileLoadingImage})
                        )
                    )
                ])
            ),
            Builder.node('div', {id:'imageDataContainer'},
                Builder.node('div',{id:'imageData'}, [
                    Builder.node('div',{id:'imageDetails'}, [
//HTH NewCap1 new sections
                        Builder.node('span',{id:'bottomNav'},
                            Builder.node('a',{id:'bottomNavClose', href: '#' },
                                Builder.node('img', { src: LightboxOptions.fileBottomNavCloseImage })
                            )
                        ),
                        Builder.node('span',{id:'caption'}),
//HTH Bottom Nav1 Begin
                        Builder.node('span',{id:'numberDisplay'}),
                        Builder.node('span',{id:'hoverNav2'}, [
                            Builder.node('a',{id:'prevLink2', href: '#' }),
                            Builder.node('a',{id:'nextLink2', href: '#' })
                        ])								
//HTH Bottom Nav1 End
                    ])
                ])
            )
        ]));


		$('overlay').hide().observe('click', (function() { this.end(); }).bind(this));
		$('lightbox').hide().observe('click', (function(event) { if (event.element().id == 'lightbox') this.end(); }).bind(this));
		$('outerImageContainer').setStyle({ width: size, height: size });
		$('prevLink').observe('click', (function(event) { event.stop(); this.changeImage(this.activeImage - 1); }).bindAsEventListener(this));
		$('nextLink').observe('click', (function(event) { event.stop(); this.changeImage(this.activeImage + 1); }).bindAsEventListener(this));
//HTH Bottom Nav2 Begin
		$('prevLink2').observe('click', (function(event) { event.stop(); this.changeImage(this.activeImage - 1); }).bindAsEventListener(this));
		$('nextLink2').observe('click', (function(event) { event.stop(); this.changeImage(this.activeImage + 1); }).bindAsEventListener(this));
//HTH Bottom Nav2 End
		$('loadingLink').observe('click', (function(event) { event.stop(); this.end(); }).bind(this));
		$('bottomNavClose').observe('click', (function(event) { event.stop(); this.end(); }).bind(this));

        var th = this;
        (function(){
            //HTH Bottom Nav3:  3 variables added -  hoverNav2 prevLink2 nextLink2
            var ids = 
                'overlay lightbox outerImageContainer imageContainer lightboxImage hoverNav prevLink nextLink hoverNav2 prevLink2 nextLink2 loading loadingLink ' + 
                'imageDataContainer imageData imageDetails caption numberDisplay bottomNav bottomNavClose';   
            $w(ids).each(function(id){ th[id] = $(id); });
        }).defer();
    },

    //
    // updateImageList()
    // Loops through anchor tags looking for 'lightbox' references and applies onclick
    // events to appropriate links. You can rerun after dynamically adding images w/ajax.
    //
    updateImageList: function() {   
        this.updateImageList = Prototype.emptyFunction;

        document.observe('click', (function(event){
            var target = event.findElement('a[rel^=lightbox]') || event.findElement('area[rel^=lightbox]');
            if (target) {
                event.stop();
                this.start(target);
            }
        }).bind(this));
    },
    
    //
    //  start()
    //  Display overlay and lightbox. If image is part of a set, add siblings to imageArray.
    //
    start: function(imageLink) {    

        $$('select', 'object', 'embed').each(function(node){ node.style.visibility = 'hidden' });

        // stretch overlay to fill page and fade in
        var arrayPageSize = this.getPageSize();
        //$('overlay').setStyle({ width: arrayPageSize[2] + 'px', height: arrayPageSize[1] + 'px' });
        $('overlay').setStyle({ /* HTH tweak: Support for Opera */
           width: (window.opera ? document.documentElement.scrollWidth : arrayPageSize[0] ) + 'px', 
           height: (window.opera ? document.documentElement.scrollHeight : arrayPageSize[1] ) + 'px' 
        });

        new Effect.Appear(this.overlay, { duration: this.overlayDuration, from: 0.0, to: LightboxOptions.overlayOpacity });

        this.imageArray = [];
        var imageNum = 0;       

        if ((imageLink.getAttribute("rel") == 'lightbox')){
		  		// HTH NewCap2: added vars to imageArray for Custom Caption via data-lbxxxx attributes, 
				//   starting at arrayvalue[5]
				//    also freeing up the native title attrib
            // if image is NOT part of a set, add single image to imageArray
            this.imageArray.push([imageLink.href, imageLink.getAttribute("data-lbtitle"),,,,imageLink.getAttribute("data-lbcap"),imageLink.getAttribute("data-lbtitlelink"),imageLink.getAttribute("data-lbimgdesc")]);
        } else {
            // if image is part of a set..
            this.imageArray = 
                $$(imageLink.tagName + '[href][rel="' + imageLink.rel + '"]').
                collect(function(anchor){ return [anchor.href, anchor.getAttribute("data-lbtitle"),,,,anchor.getAttribute("data-lbcap"),anchor.getAttribute("data-lbtitlelink"),anchor.getAttribute("data-lbimgdesc")]; }).
                uniq();
            
            while (this.imageArray[imageNum][0] != imageLink.href) { imageNum++; }
        }
		  
        // calculate top and left offset for the lightbox 
        var arrayPageScroll = document.viewport.getScrollOffsets();
        var lightboxTop = arrayPageScroll[1] + (document.viewport.getHeight() / 15);
        var lightboxLeft = arrayPageScroll[0];
        this.lightbox.setStyle({ top: lightboxTop + 'px', left: lightboxLeft + 'px' }).show();
//SEB2 BEGIN
        if (LightboxOptions.featBrowser == true) { Event.observe(window, 'resize', (function(e) {this.adjustImageSize(true); }).bind(this)); }
//SEB2 END
        this.changeImage(imageNum);
    },

    //
    //  changeImage()
    //  Hide most elements and preload image in preparation for resizing image container.
    //
    changeImage: function(imageNum) {   
        
        this.activeImage = imageNum; // update global var

        // hide elements during transition
        if (LightboxOptions.animate) this.loading.show();
        this.lightboxImage.hide();
        this.hoverNav.hide();
        this.prevLink.hide();
        this.nextLink.hide();
		 // HTH: Opera "hack" moved back here and recoded so not interefering with other mods or browsers
		 //   (the new place it was moved to (by another modder) caused problems when otherwise tweaking the code)
		 //  Opera9 does not currently support scriptaculous opacity and appear fx
        window.opera ? this.imageDataContainer.setStyle({opacity: .0001}) : this.imageDataContainer.hide() ;
        this.bottomNavClose.hide();   //HTH Show/Hide1 Additions: If adding positioning to objects (like images I added), do this 
                                                 //or they will flash in IE(first witnessed in IE8
        this.hoverNav2.hide();   //HTH Bottom Nav4a 
        this.prevLink2.hide();   //HTH Bottom Nav4b
        this.nextLink2.hide();   //HTH Bottom Nav4c
        this.numberDisplay.hide();      
        
        var imgPreloader = new Image();
        
        // once image is preloaded, resize image container
        imgPreloader.onload = (function(){
            this.lightboxImage.src = this.imageArray[this.activeImage][0];
//SEB3 BEGIN   (commented out replaced section)
            /*Bug Fixed by Andy Scott*/
            // this.lightboxImage.width = imgPreloader.width;
            // this.lightboxImage.height = imgPreloader.height;
            /*End of Bug Fix*/
            // this.resizeImageContainer(imgPreloader.width, imgPreloader.height);
            this.imageArray[this.activeImage][2] = imgPreloader.width;
            this.imageArray[this.activeImage][3] = imgPreloader.height;
            this.adjustImageSize(false);
//SEB3 END
        }).bind(this);
        imgPreloader.src = this.imageArray[this.activeImage][0];
    },

//SEB4 BEGIN
    //
    //  adjustImageSize()
    //  adjust image size if option featBrowser is set to true
    //  HTH SEB note: minor adjustments made, plus needs coding for resizing next/prev div overlays
    //
    adjustImageSize: function( recall ) {
        // get image size
        imgWidth = this.imageArray[this.activeImage][2];
        imgHeight = this.imageArray[this.activeImage][3];
        var arrayPageSize = this.getPageSize();

        // adjust image size if featBrowser option is set to true
        if (LightboxOptions.featBrowser == true) {
          // calculate proportions 
          var imageProportion = imgWidth / imgHeight;
          var winProportion = arrayPageSize[2] / arrayPageSize[3];

          if (imageProportion > winProportion) {
            // calculate max width base on page width
            var maxWidth = arrayPageSize[2] - (LightboxOptions.borderSize * 4) - (LightboxOptions.breathingSize * 2);
            var maxHeight = Math.round(maxWidth / imageProportion);
          } else {
            // calculate maw height base on page height
            //HTH NewCap3 - you can add some px to LightboxOptions.breathingSize to compensate for caption height
            var maxHeight = arrayPageSize[3] - (LightboxOptions.borderSize * 5) - (arrayPageSize[3] / 15) - (LightboxOptions.breathingSize+LightboxOptions.breathingSizeCaption); //HTH added +X0 for some caption spacing on resize. Typically nothing is added here. YOU SET THIS IN THE CONFIGURATION SECTION - These are just notes.
            var maxWidth = Math.round(maxHeight * imageProportion);
          }
          if (imgWidth > maxWidth || imgHeight > maxHeight) {
            imgWidth = maxWidth;
            imgHeight = maxHeight-73;  //HTH Bottom Nav5: Add 63px-73px++ to compensate for addition of Bottom Nav Buttons
          }
        }
        //HTH SEB: truncates overlay, so added width and using pageHeight instead of windowHeight (temporarily?)
        // HTH Update: Opera cannot set real win/pag/doc height when using "html height:100%" in base css
        // Added code below to get around the problem ;^)
        // HTH SEB- following seems to work better, and not as well with the "this" keyword - go figure? maybe some other unrelated issue?
        //ORG this.overlay.setStyle({ height: arrayPageSize[3] + 'px' });
		  $('overlay').setStyle({ width: arrayPageSize[2] + 'px', height: (window.opera ? document.documentElement.scrollHeight : arrayPageSize[1] ) + 'px' });
        this.lightboxImage.setStyle({ height: imgHeight + 'px', width: imgWidth + 'px'});

        if (recall == true) {
          this.outerImageContainer.setStyle({width: (imgWidth + (LightboxOptions.borderSize * 2)) + 'px', height: (imgHeight + (LightboxOptions.borderSize * 2)) + 'px'});
          this.imageDataContainer.setStyle({ width: (imgWidth + (LightboxOptions.borderSize * 2)) + 'px' });
			 // HTH SEB: Next/Prev Overlay Fix (2 lines added) 
			 //   Note: because p/n classes have height set to 100% in css, the fix may be more easily addressed (use less code) in resizeImageContainer, but adding this code certainly does the trick.  What I don't know is if, due to Cross browser needs perhaps?, this class may require the conversion into px, rather than relying on % value - I will be testing later. 
          this.prevLink.setStyle({ height: (imgHeight) + 'px' });
          this.nextLink.setStyle({ height: (imgHeight) + 'px' });
        } else {
          this.resizeImageContainer(imgWidth, imgHeight);
        }
        
        // HTH CustCapTweak1 Begin: set variable for "Click for full size version" link in 'updateDetails()' section
        if  ((imgWidth == this.imageArray[this.activeImage][2]) && (imgHeight = this.imageArray[this.activeImage][3]))
        {
           this.viewlrgrtxt = '';
        }  else {
        // EDIT THIS STRING FOR CUSTOM CAPTION AND/OR FULL-SIZE LINK in Number of Images Caption Space  
        // Note: popup-this-href is a simple function - I have included it in the header. Be creative with your own script here! ;^)
        this.viewlrgrtxt = ' &nbsp;&nbsp;&rarr;&nbsp;<a href="' + this.imageArray[this.activeImage][0] + '"  onclick="popUp(this.href); return false;" rel="nofollow" title="pops up">Click here to view Full-size</a>';
        }
        //HTH experimental: update 'click for full size link' in Img # of # section when dynamically resizing
        if (this.imageArray.length > 1){
           this.numberDisplay.update( LightboxOptions.labelImage + ' ' + (this.activeImage + 1) + ' ' + LightboxOptions.labelOf + '  ' + this.imageArray.length + '  ' + this.viewlrgrtxt).show();
        } else {
           this.numberDisplay.update(this.viewlrgrtxt).show();
        }
		  // HTH CustCapTweak1 End

    },
//SEB4 End

    //
    //  resizeImageContainer()
    //
    resizeImageContainer: function(imgWidth, imgHeight) {

        // get current width and height
        var widthCurrent  = this.outerImageContainer.getWidth();
        var heightCurrent = this.outerImageContainer.getHeight();

        // get new width and height
        var widthNew  = (imgWidth  + LightboxOptions.borderSize * 2);
        var heightNew = (imgHeight + LightboxOptions.borderSize * 2);

        // scalars based on change from old to new
        var xScale = (widthNew  / widthCurrent)  * 100;
        var yScale = (heightNew / heightCurrent) * 100;

        // calculate size difference between new and old image, and resize if necessary
        var wDiff = widthCurrent - widthNew;
        var hDiff = heightCurrent - heightNew;

        if (hDiff != 0) new Effect.Scale(this.outerImageContainer, yScale, {scaleX: false, scaleContent:false, duration: this.resizeDuration, queue: 'front'});  /* HTH bug fix, added scaleContent to suppress font resizing in fluid designs that offsets conntent here */
        if (wDiff != 0) new Effect.Scale(this.outerImageContainer, xScale, {scaleY: false, scaleContent:false, duration: this.resizeDuration, delay: this.resizeDuration});   /* HTH bug fix, added scaleContent to suppress font resizing in fluid designs that offsets conntent here */

        // if new and old image are same size and no scaling transition is necessary, 
        // do a quick pause to prevent image flicker.
        var timeout = 0;
        if ((hDiff == 0) && (wDiff == 0)){
            timeout = 100;
            if (Prototype.Browser.IE) timeout = 250;   
        }

        (function(){
            this.prevLink.setStyle({ height: imgHeight + 'px' });
            this.nextLink.setStyle({ height: imgHeight + 'px' });
            this.imageDataContainer.setStyle({ width: widthNew + 'px' });

            this.showImage();
        }).bind(this).delay(timeout / 1000);
    },
    
    //
    //  showImage()
    //  Display image and begin preloading neighbors.
    //
    showImage: function(){
        this.loading.hide();
        new Effect.Appear(this.lightboxImage, { 
            duration: this.resizeDuration, 
            queue: 'end', 
            afterFinish: (function(){ this.updateDetails(); }).bind(this) 
        });
        this.preloadNeighborImages();
    },

    //
    //  updateDetails()
    //  Display caption, image number, and bottom nav.
    //
    updateDetails: function() {

		  // HTH NewCap 4 Begin: set lbCaption CUSTOMIZATIONS  
          // **EDIT FOR CREATIVE APPLICATION** Set to '' (for blank) OR CUSTOMIZE HOW YOU WISH!
		  //Customize lbTitle [1]
        if (this.imageArray[this.activeImage][1]!=null && this.imageArray[this.activeImage][1]!="")
		  {
		  		this.datalbTitle = this.imageArray[this.activeImage][1];
		  } else {
		  		this.datalbTitle = '';
			}
	
		  //Customize lbTitleLink [6]  -set a link format for the lbTitle (if you like)
		  //Setting a mylink value in attrib data-lbtitlelink="mylink" will apply that link to the lbTitle
		  //Get creative and give this its own attributes, javascript, php, etc
		  //Example Resulte: <a href="link"  title="To Gallery View" >PicTitle <br /> Click Here for Photo Gallery</a>
        if (this.imageArray[this.activeImage][6]!=null && this.imageArray[this.activeImage][6]!="")
		  {
		  		this.datalbTitle = this.datalbTitle + '<br /><a href="' + this.imageArray[this.activeImage][6] + '"   title="To Gallery View">Click Here for Photo Gallery</a>';
			}
			

		  //Customize lbDescription  (data-lbcap = [5]  Example: red description text
        if (this.imageArray[this.activeImage][5]!=null && this.imageArray[this.activeImage][5]!="")
		  {
		  		this.datalbcap = ' <br /><span style="color:red; font-weight: normal; font-family: Verdana, Geneva, Arial, Helvetica;">' + this.imageArray[this.activeImage][5] + '</span>';
		  } else {
		  		this.datalbcap = '';
			}
		  
		  //Customize lbDescription  [7]
        if (this.imageArray[this.activeImage][6]!=null && this.imageArray[this.activeImage][6]!="")
		  {
		  		this.datalbImgDesc = ' <br /><span style="color:green; font-weight: normal; font-family: Palatino, Times, serif;">' + this.imageArray[this.activeImage][6] + '</span>';
		  } else {
		  		this.datalbImgDesc = 'XXXXXXXXXXXXXXXXXXXXXXX';
			}

        //display pic description lbImgDesc
        //this.lbImgDesc.update(this.datalbImgDesc).show();

        // HTH NewCap 4 End: set lbCaption Customizations Section 

        // HTH Show Close1: Use this when CLoseButton Placement is on the top. Use HTH Show Close2 when its on the bottom
        // Fades in just a bit quick in Opera 9, but 10 and up look good.
        this.bottomNavClose.show();      //HTH Show/Hide1 Additions: If adding positioning to objects (like images I added) 
                                                     // you need to manage this, or they will flash in IE(first witnessed in IE8)
		  
        // display pic caption (using HTH variables now)
        // if pic caption blank - repair (removed - done differently in this HTH version): do not display caption of previous image if new image has none
        this.caption.update(this.datalbTitle + this.datalbcap).show();
        //  this.caption.update(this.datalbTitle ? this.datalbTitle + this.datalbcap : "").show();
        //  ORG this.caption.update(this.imageArray[this.activeImage][1]).show();
        //SEB5a wkup to include link on Name Caption -not used (but you can if you like, so I left the notes in). 
        //         Moved to -adjustimagesize function, see above)>>
        //Note: I ended up not using this in the caption space, but only in the 'display # of images' space'. see next.
        //   :  ? this.imageArray[this.activeImage][1] + '" <a href="' + this.imageArray[this.activeImage][0] + '" rel="nofollow">Click here to view Full-size</a>"' :
        //replaces:    ? this.imageArray[this.activeImage][1] :
        
        // if image is part of set display 'Image x of x' 
        // HTH NewCap 5 Begin: apply variable for 'Click for full size version' link set in AutoResize section ~line 423
        //Note: I prefer to do this in the image number zone (here), SO I had to edit to show when only a single image is displayed...
        if (this.imageArray.length > 1){
           this.numberDisplay.update( LightboxOptions.labelImage + ' ' + (this.activeImage + 1) + ' ' + LightboxOptions.labelOf + '  ' + this.imageArray.length + '  ' + this.viewlrgrtxt).show();
        //SEB5b notes..  to include link on Image # Caption  
        // (Moved to -adjustimagesize function, see HTH CustCapTweak1 above) >>
        // :   this.numberDisplay.update( LightboxOptions.labelImage + ' ' + (this.activeImage + 1) + ' ' + LightboxOptions.labelOf + ' ' + this.imageArray.length+ '" <a href="' + this.imageArray[this.activeImage][0] + '" rel="nofollow">Click here to view Full-size</a>"').show();
        } else {
           this.numberDisplay.update(this.viewlrgrtxt).show();
        }
        
        //HTH NewCap 5 End
		  
        //HTH: Opera code moved back to original location and also fixed for proper application 

        new Effect.Parallel(
            [ 
                new Effect.SlideDown(this.imageDataContainer, { sync: true, duration: this.resizeDuration, from: 0.0, to: 1.0 }), 
                new Effect.Appear(this.imageDataContainer, { sync: true, duration: this.resizeDuration }) 
            ], 
            { 
                duration: this.resizeDuration, 
                afterFinish: (function() {
	                // update overlay size and update nav  //HTH note: for when LB extends below page bottom
	                var arrayPageSize = this.getPageSize();
                   this.overlay.setStyle({ /* HTH: Help (esp for Opera 10++) for ReDraw Overlay to bottom of page @post-LB-popup-img display */
                      width: (window.opera ? document.documentElement.scrollWidth : arrayPageSize[0] ) + 'px', 
                      height: (window.opera ? document.documentElement.scrollHeight : arrayPageSize[1] ) + 'px' 
                   });
	                this.updateNav();
                }).bind(this)
            } 
        );
    },

    //
    //  updateNav()
    //  Display appropriate previous and next hover navigation.
    //
    updateNav: function() {

        this.hoverNav.show();               
        if (this.imageArray.length > 1) this.hoverNav2.show();     //HTH Bottom Nav6a             

        // if not first image in set, display prev image button
        if (this.activeImage > 0) this.prevLink.show();
        if (this.activeImage > 0) this.prevLink2.show();   //HTH Bottom Nav6b

        // if not last image in set, display next image button
        if (this.activeImage < (this.imageArray.length - 1)) this.nextLink.show();
        if (this.activeImage < (this.imageArray.length - 1)) this.nextLink2.show();   //HTH Bottom Nav6c
        
        // HTH Show Close2: Use this when CLoseButton Placement is on the Bottom. 
        // You may Use HTH Show Close1 when its on the top. This way Captions wrap prior to rendering on screen ;^)
        // this.bottomNavClose.show();   //HTH Show/Hide1 Additions: If adding positioning to objects (like images I added) 
                                                     // you need to manage this, or they will flash in IE(first witnessed in IE8)
        this.enableKeyboardNav();
    },

    //
    //  enableKeyboardNav()
    //
    enableKeyboardNav: function() {
        document.observe('keydown', this.keyboardAction); 
    },

    //
    //  disableKeyboardNav()
    //
    disableKeyboardNav: function() {
        document.stopObserving('keydown', this.keyboardAction); 
    },

    //
    //  keyboardAction()
    //
    keyboardAction: function(event) {
        var keycode = event.keyCode;

        var escapeKey;
        if (event.DOM_VK_ESCAPE) {  // mozilla
            escapeKey = event.DOM_VK_ESCAPE;
        } else { // ie
            escapeKey = 27;
        }

        var key = String.fromCharCode(keycode).toLowerCase();
        
        if (key.match(/x|o|c/) || (keycode == escapeKey)){ // close lightbox
            this.end();
        } else if ((key == 'p') || (keycode == 37)){ // display previous image
            if (this.activeImage != 0){
                this.disableKeyboardNav();
                this.changeImage(this.activeImage - 1);
            }
        } else if ((key == 'n') || (keycode == 39)){ // display next image
            if (this.activeImage != (this.imageArray.length - 1)){
                this.disableKeyboardNav();
                this.changeImage(this.activeImage + 1);
            }
        }
    },

    //
    //  preloadNeighborImages()
    //  Preload previous and next images.
    //
    preloadNeighborImages: function(){
        var preloadNextImage, preloadPrevImage;
        if (this.imageArray.length > this.activeImage + 1){
            preloadNextImage = new Image();
            preloadNextImage.src = this.imageArray[this.activeImage + 1][0];
        }
        if (this.activeImage > 0){
            preloadPrevImage = new Image();
            preloadPrevImage.src = this.imageArray[this.activeImage - 1][0];
        }
    
    },

    //
    //  end()
    //
    end: function() {
        this.disableKeyboardNav();
        this.bottomNavClose.hide();   //HTH Show/Hide2 Additions: If adding positioning to objects (like images I added), do this 
        this.prevLink2.hide();            //or they will flash in IE
        this.nextLink2.hide();            //
        this.lightbox.hide();
        new Effect.Fade(this.overlay, { duration: this.overlayDuration });
        $$('select', 'object', 'embed').each(function(node){ node.style.visibility = 'visible' });
    },

    //
    //  getPageSize()
    //
    getPageSize: function() {
	        
	     var xScroll, yScroll;
		
		if (window.innerHeight && window.scrollMaxY) {	
			xScroll = window.innerWidth + window.scrollMaxX;
			yScroll = window.innerHeight + window.scrollMaxY;
		} else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
			xScroll = document.body.scrollWidth;
			yScroll = document.body.scrollHeight;
		} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
			xScroll = document.body.offsetWidth;
			yScroll = document.body.offsetHeight;
		}
		
		var windowWidth, windowHeight;
		
		if (self.innerHeight) {	// all except Explorer
			if(document.documentElement.clientWidth){
				windowWidth = document.documentElement.clientWidth; 
			} else {
				windowWidth = self.innerWidth;
			}
			windowHeight = self.innerHeight;
		} else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
			windowWidth = document.documentElement.clientWidth;
			windowHeight = document.documentElement.clientHeight;
		} else if (document.body) { // other Explorers
			windowWidth = document.body.clientWidth;
			windowHeight = document.body.clientHeight;
		}	

		// for small pages with total height less then height of the viewport
		if(yScroll < windowHeight){
			pageHeight = windowHeight;
		} else { 
			pageHeight = yScroll;
		}
	
		// for small pages with total width less then width of the viewport
		if(xScroll < windowWidth){	
			pageWidth = xScroll;		
		} else {
			pageWidth = windowWidth;
		}
		// SEB6  windowWidth,windowHeight added back in for resizing image
		return [pageWidth,pageHeight,windowWidth,windowHeight];
	}
}

document.observe('dom:loaded', function () { new Lightbox(); });
