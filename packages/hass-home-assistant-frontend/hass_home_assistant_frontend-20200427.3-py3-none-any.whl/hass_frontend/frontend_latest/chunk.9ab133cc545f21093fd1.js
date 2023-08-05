/*! For license information please see chunk.9ab133cc545f21093fd1.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[154,158],{133:function(e,t,n){"use strict";n(4),n(33),n(103),n(73),n(137),n(107),n(47),n(160),n(161);var r=n(60),a=n(38),o=n(63),i=n(64),s=n(5),l=n(1),c=n(39),u=n(3);Object(s.a)({_template:u.a`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <!-- this div fulfills an a11y requirement for combobox, do not remove -->
    <span role="button"></span>
    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[r.a,a.a,o.a,i.a],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},hostAttributes:{role:"combobox","aria-autocomplete":"none","aria-haspopup":"true"},observers:["_selectedItemChanged(selectedItem)"],attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=Object(l.a)(this.$.content).getDistributedNodes(),t=0,n=e.length;t<n;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){c.c(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},160:function(e,t,n){"use strict";n(95);const r=document.createElement("template");r.setAttribute("style","display: none;"),r.innerHTML='<iron-iconset-svg name="paper-dropdown-menu" size="24">\n<svg><defs>\n<g id="arrow-drop-down"><path d="M7 10l5 5 5-5z"></path></g>\n</defs></svg>\n</iron-iconset-svg>',document.head.appendChild(r.content)},161:function(e,t,n){"use strict";n(47);const r=document.createElement("template");r.setAttribute("style","display: none;"),r.innerHTML='<dom-module id="paper-dropdown-menu-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: inline-block;\n        position: relative;\n        text-align: left;\n\n        /* NOTE(cdata): Both values are needed, since some phones require the\n         * value to be `transparent`.\n         */\n        -webkit-tap-highlight-color: rgba(0,0,0,0);\n        -webkit-tap-highlight-color: transparent;\n\n        --paper-input-container-input: {\n          overflow: hidden;\n          white-space: nowrap;\n          text-overflow: ellipsis;\n          max-width: 100%;\n          box-sizing: border-box;\n          cursor: pointer;\n        };\n\n        @apply --paper-dropdown-menu;\n      }\n\n      :host([disabled]) {\n        @apply --paper-dropdown-menu-disabled;\n      }\n\n      :host([noink]) paper-ripple {\n        display: none;\n      }\n\n      :host([no-label-float]) paper-ripple {\n        top: 8px;\n      }\n\n      paper-ripple {\n        top: 12px;\n        left: 0px;\n        bottom: 8px;\n        right: 0px;\n\n        @apply --paper-dropdown-menu-ripple;\n      }\n\n      paper-menu-button {\n        display: block;\n        padding: 0;\n\n        @apply --paper-dropdown-menu-button;\n      }\n\n      paper-input {\n        @apply --paper-dropdown-menu-input;\n      }\n\n      iron-icon {\n        color: var(--disabled-text-color);\n\n        @apply --paper-dropdown-menu-icon;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(r.content)},231:function(e,t,n){"use strict";n.d(t,"a",function(){return S});class r extends TypeError{static format(e){const{type:t,path:n,value:r}=e;return`Expected a value of type \`${t}\`${n.length?` for \`${n.join(".")}\``:""} but received \`${JSON.stringify(r)}\`.`}constructor(e){super(r.format(e));const{data:t,path:n,value:a,reason:o,type:i,errors:s=[]}=e;this.data=t,this.path=n,this.value=a,this.reason=o,this.type=i,this.errors=s,s.length||s.push(this),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=(new Error).stack}}var a=Object.prototype.toString,o=function(e){if(void 0===e)return"undefined";if(null===e)return"null";var t=typeof e;if("boolean"===t)return"boolean";if("string"===t)return"string";if("number"===t)return"number";if("symbol"===t)return"symbol";if("function"===t)return"GeneratorFunction"===i(e)?"generatorfunction":"function";if(function(e){return Array.isArray?Array.isArray(e):e instanceof Array}(e))return"array";if(function(e){if(e.constructor&&"function"==typeof e.constructor.isBuffer)return e.constructor.isBuffer(e);return!1}(e))return"buffer";if(function(e){try{if("number"==typeof e.length&&"function"==typeof e.callee)return!0}catch(t){if(-1!==t.message.indexOf("callee"))return!0}return!1}(e))return"arguments";if(function(e){return e instanceof Date||"function"==typeof e.toDateString&&"function"==typeof e.getDate&&"function"==typeof e.setDate}(e))return"date";if(function(e){return e instanceof Error||"string"==typeof e.message&&e.constructor&&"number"==typeof e.constructor.stackTraceLimit}(e))return"error";if(function(e){return e instanceof RegExp||"string"==typeof e.flags&&"boolean"==typeof e.ignoreCase&&"boolean"==typeof e.multiline&&"boolean"==typeof e.global}(e))return"regexp";switch(i(e)){case"Symbol":return"symbol";case"Promise":return"promise";case"WeakMap":return"weakmap";case"WeakSet":return"weakset";case"Map":return"map";case"Set":return"set";case"Int8Array":return"int8array";case"Uint8Array":return"uint8array";case"Uint8ClampedArray":return"uint8clampedarray";case"Int16Array":return"int16array";case"Uint16Array":return"uint16array";case"Int32Array":return"int32array";case"Uint32Array":return"uint32array";case"Float32Array":return"float32array";case"Float64Array":return"float64array"}if(function(e){return"function"==typeof e.throw&&"function"==typeof e.return&&"function"==typeof e.next}(e))return"generator";switch(t=a.call(e)){case"[object Object]":return"object";case"[object Map Iterator]":return"mapiterator";case"[object Set Iterator]":return"setiterator";case"[object String Iterator]":return"stringiterator";case"[object Array Iterator]":return"arrayiterator"}return t.slice(8,-1).toLowerCase().replace(/\s/g,"")};function i(e){return e.constructor?e.constructor.name:null}const s="@@__STRUCT__@@",l="@@__KIND__@@";function c(e){return!(!e||!e[s])}function u(e,t){return"function"==typeof e?e(t):e}var p=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e};class d{constructor(e,t,n){this.name=e,this.type=t,this.validate=n}}function h(e,t,n){if(c(e))return e[l];if(e instanceof d)return e;switch(o(e)){case"array":return e.length>1?w(e,t,n):v(e,t,n);case"function":return y(e,t,n);case"object":return m(e,t,n);case"string":{let r,a=!0;if(e.endsWith("?")&&(a=!1,e=e.slice(0,-1)),e.includes("|")){r=x(e.split(/\s*\|\s*/g),t,n)}else if(e.includes("&")){r=$(e.split(/\s*&\s*/g),t,n)}else r=g(e,t,n);return a||(r=b(r,void 0,n)),r}}throw new Error(`Invalid schema: ${e}`)}function f(e,t,n){if("array"!==o(e))throw new Error(`Invalid schema: ${e}`);const r=e.map(e=>{try{return JSON.stringify(e)}catch(t){return String(e)}}).join(" | ");return new d("enum",r,(n=u(t))=>e.includes(n)?[void 0,n]:[{data:n,path:[],value:n,type:r}])}function y(e,t,n){if("function"!==o(e))throw new Error(`Invalid schema: ${e}`);return new d("function","<function>",(n=u(t),r)=>{const a=e(n,r);let i,s={path:[],reason:null};switch(o(a)){case"boolean":i=a;break;case"string":i=!1,s.reason=a;break;case"object":i=!1,s=p({},s,a);break;default:throw new Error(`Invalid result: ${a}`)}return i?[void 0,n]:[p({type:"<function>",value:n,data:n},s)]})}function v(e,t,n){if("array"!==o(e)||1!==e.length)throw new Error(`Invalid schema: ${e}`);const r=g("array",void 0,n),a=h(e[0],void 0,n),i=`[${a.type}]`;return new d("list",i,(e=u(t))=>{const[n,o]=r.validate(e);if(n)return n.type=i,[n];e=o;const s=[],l=[];for(let t=0;t<e.length;t++){const n=e[t],[r,o]=a.validate(n);r?(r.errors||[r]).forEach(n=>{n.path=[t].concat(n.path),n.data=e,s.push(n)}):l[t]=o}if(s.length){const e=s[0];return e.errors=s,[e]}return[void 0,l]})}function m(e,t,n){if("object"!==o(e))throw new Error(`Invalid schema: ${e}`);const r=g("object",void 0,n),a=[],i={};for(const o in e){a.push(o);const t=h(e[o],void 0,n);i[o]=t}const s=`{${a.join()}}`;return new d("object",s,(e=u(t))=>{const[n]=r.validate(e);if(n)return n.type=s,[n];const a=[],o={},l=Object.keys(e),c=Object.keys(i);if(new Set(l.concat(c)).forEach(n=>{let r=e[n];const s=i[n];if(void 0===r&&(r=u(t&&t[n],e)),!s){const t={data:e,path:[n],value:r};return void a.push(t)}const[l,c]=s.validate(r,e);l?(l.errors||[l]).forEach(t=>{t.path=[n].concat(t.path),t.data=e,a.push(t)}):(n in e||void 0!==c)&&(o[n]=c)}),a.length){const e=a[0];return e.errors=a,[e]}return[void 0,o]})}function b(e,t,n){return x([e,"undefined"],t,n)}function g(e,t,n){if("string"!==o(e))throw new Error(`Invalid schema: ${e}`);const{types:r}=n,a=r[e];if("function"!==o(a))throw new Error(`Invalid type: ${e}`);const i=y(a,t),s=e;return new d("scalar",s,e=>{const[t,n]=i.validate(e);return t?(t.type=s,[t]):[void 0,n]})}function w(e,t,n){if("array"!==o(e))throw new Error(`Invalid schema: ${e}`);const r=e.map(e=>h(e,void 0,n)),a=g("array",void 0,n),i=`[${r.map(e=>e.type).join()}]`;return new d("tuple",i,(e=u(t))=>{const[n]=a.validate(e);if(n)return n.type=i,[n];const o=[],s=[],l=Math.max(e.length,r.length);for(let t=0;t<l;t++){const n=r[t],a=e[t];if(!n){const n={data:e,path:[t],value:a};s.push(n);continue}const[i,l]=n.validate(a);i?(i.errors||[i]).forEach(n=>{n.path=[t].concat(n.path),n.data=e,s.push(n)}):o[t]=l}if(s.length){const e=s[0];return e.errors=s,[e]}return[void 0,o]})}function x(e,t,n){if("array"!==o(e))throw new Error(`Invalid schema: ${e}`);const r=e.map(e=>h(e,void 0,n)),a=r.map(e=>e.type).join(" | ");return new d("union",a,(e=u(t))=>{const n=[];for(const t of r){const[r,a]=t.validate(e);if(!r)return[void 0,a];n.push(r)}return n[0].type=a,n})}function $(e,t,n){if("array"!==o(e))throw new Error(`Invalid schema: ${e}`);const r=e.map(e=>h(e,void 0,n)),a=r.map(e=>e.type).join(" & ");return new d("intersection",a,(e=u(t))=>{let n=e;for(const t of r){const[e,r]=t.validate(n);if(e)return e.type=a,[e];n=r}return[void 0,n]})}const _={any:h,dict:function(e,t,n){if("array"!==o(e)||2!==e.length)throw new Error(`Invalid schema: ${e}`);const r=g("object",void 0,n),a=h(e[0],void 0,n),i=h(e[1],void 0,n),s=`dict<${a.type},${i.type}>`;return new d("dict",s,e=>{const n=u(t);e=n?p({},n,e):e;const[o]=r.validate(e);if(o)return o.type=s,[o];const l={},c=[];for(let t in e){const n=e[t],[r,o]=a.validate(t);if(r){(r.errors||[r]).forEach(n=>{n.path=[t].concat(n.path),n.data=e,c.push(n)});continue}t=o;const[s,u]=i.validate(n);s?(s.errors||[s]).forEach(n=>{n.path=[t].concat(n.path),n.data=e,c.push(n)}):l[t]=u}if(c.length){const e=c[0];return e.errors=c,[e]}return[void 0,l]})},enum:f,enums:function(e,t,n){return v([f(e,void 0)],t,n)},function:y,instance:function(e,t,n){const r=`instance<${e.name}>`;return new d("instance",r,(n=u(t))=>n instanceof e?[void 0,n]:[{data:n,path:[],value:n,type:r}])},interface:function(e,t,n){if("object"!==o(e))throw new Error(`Invalid schema: ${e}`);const r=[],a={};for(const o in e){r.push(o);const t=h(e[o],void 0,n);a[o]=t}const i=`{${r.join()}}`;return new d("interface",i,e=>{const n=u(t);e=n?p({},n,e):e;const r=[],o=e;for(const i in a){let n=e[i];const s=a[i];void 0===n&&(n=u(t&&t[i],e));const[l,c]=s.validate(n,e);l?(l.errors||[l]).forEach(t=>{t.path=[i].concat(t.path),t.data=e,r.push(t)}):(i in e||void 0!==c)&&(o[i]=c)}if(r.length){const e=r[0];return e.errors=r,[e]}return[void 0,o]})},lazy:function(e,t,n){if("function"!==o(e))throw new Error(`Invalid schema: ${e}`);let r,a;return r=new d("lazy","lazy...",t=>(a=e(),r.name=a.kind,r.type=a.type,r.validate=a.validate,r.validate(t)))},list:v,literal:function(e,t,n){const r=`literal: ${JSON.stringify(e)}`;return new d("literal",r,(n=u(t))=>n===e?[void 0,n]:[{data:n,path:[],value:n,type:r}])},object:m,optional:b,partial:function(e,t,n){if("object"!==o(e))throw new Error(`Invalid schema: ${e}`);const r=g("object",void 0,n),a=[],i={};for(const o in e){a.push(o);const t=h(e[o],void 0,n);i[o]=t}const s=`{${a.join()},...}`;return new d("partial",s,(e=u(t))=>{const[n]=r.validate(e);if(n)return n.type=s,[n];const a=[],o={};for(const r in i){let n=e[r];const s=i[r];void 0===n&&(n=u(t&&t[r],e));const[l,c]=s.validate(n,e);l?(l.errors||[l]).forEach(t=>{t.path=[r].concat(t.path),t.data=e,a.push(t)}):(r in e||void 0!==c)&&(o[r]=c)}if(a.length){const e=a[0];return e.errors=a,[e]}return[void 0,o]})},scalar:g,tuple:w,union:x,intersection:$,dynamic:function(e,t,n){if("function"!==o(e))throw new Error(`Invalid schema: ${e}`);return new d("dynamic","dynamic...",(n=u(t),r)=>{const a=e(n,r);if("function"!==o(a))throw new Error(`Invalid schema: ${a}`);const[i,s]=a.validate(n);return i?[i]:[void 0,s]})}},E={any:e=>void 0!==e};function S(e={}){const t=p({},E,e.types||{});function n(e,n,a={}){c(e)&&(e=e.schema);const o=_.any(e,n,p({},a,{types:t}));function i(e){if(this instanceof i)throw new Error("Invalid `new` keyword!");return i.assert(e)}return Object.defineProperty(i,s,{value:!0}),Object.defineProperty(i,l,{value:o}),i.kind=o.name,i.type=o.type,i.schema=e,i.defaults=n,i.options=a,i.assert=(e=>{const[t,n]=o.validate(e);if(t)throw new r(t);return n}),i.test=(e=>{const[t]=o.validate(e);return!t}),i.validate=(e=>{const[t,n]=o.validate(e);return t?[new r(t)]:[void 0,n]}),i}return Object.keys(_).forEach(e=>{const r=_[e];n[e]=((e,a,o)=>{return n(r(e,a,p({},o,{types:t})),a,o)})}),n}["arguments","array","boolean","buffer","error","float32array","float64array","function","generatorfunction","int16array","int32array","int8array","map","null","number","object","promise","regexp","set","string","symbol","uint16array","uint32array","uint8array","uint8clampedarray","undefined","weakmap","weakset"].forEach(e=>{E[e]=(t=>o(t)===e)}),E.date=(e=>"date"===o(e)&&!isNaN(e));S()},261:function(e,t,n){"use strict";n(4),n(51);var r=n(38),a=n(64),o=n(5),i=n(1),s=n(3);Object(o.a)({_template:s.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[a.a,r.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=a.a.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=Object(i.a)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});n(125),n(126),n(127);var l=n(63),c=n(108);Object(o.a)({_template:s.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[c.a,l.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})}}]);
//# sourceMappingURL=chunk.9ab133cc545f21093fd1.js.map