/*! For license information please see chunk.8a77bebdcfb11c7735aa.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[139],{200:function(e,t,i){"use strict";i.d(t,"b",function(){return s}),i.d(t,"a",function(){return o});i(4);var r=i(97),n=i(1);const s={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(e,t){t&&(e?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(e){this.closingReason=this.closingReason||{},this.closingReason.confirmed=e},_onDialogClick:function(e){for(var t=Object(n.a)(e).path,i=0,r=t.indexOf(this);i<r;i++){var s=t[i];if(s.hasAttribute&&(s.hasAttribute("dialog-dismiss")||s.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(s.hasAttribute("dialog-confirm")),this.close(),e.stopPropagation();break}}}},o=[r.a,s]},202:function(e,t,i){"use strict";i(4),i(74),i(163);var r=i(5),n=i(3),s=i(141);const o=n.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
`;o.setAttribute("strip-whitespace",""),Object(r.a)({_template:o,is:"paper-spinner",behaviors:[s.a]})},213:function(e,t,i){"use strict";i(4),i(51),i(47),i(52),i(96);const r=document.createElement("template");r.setAttribute("style","display: none;"),r.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(r.content)},214:function(e,t,i){"use strict";i(215);var r=i(80),n=i(142),s=i(1);const o={getTabbableNodes:function(e){var t=[];return this._collectTabbableNodes(e,t)?n.a._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!n.a._isVisible(e))return!1;var i,r=e,o=n.a._normalizedTabIndex(r),a=o>0;o>=0&&t.push(r),i="content"===r.localName||"slot"===r.localName?Object(s.a)(r).getDistributedNodes():Object(s.a)(r.shadowRoot||r.root||r).children;for(var l=0;l<i.length;l++)a=this._collectTabbableNodes(i[l],t)||a;return a}},a=customElements.get("paper-dialog"),l={get _focusableNodes(){return o.getTabbableNodes(this)}};customElements.define("ha-paper-dialog",class extends(Object(r.b)([l],a)){})},215:function(e,t,i){"use strict";i(4),i(213);var r=i(136),n=i(200),s=i(5),o=i(3);Object(s.a)({_template:o.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[n.a,r.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},234:function(e,t,i){"use strict";i(4),i(51),i(47);var r=i(200),n=i(5),s=i(3);Object(n.a)({_template:s.a`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(r.b)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},250:function(e,t,i){"use strict";i.d(t,"d",function(){return r}),i.d(t,"a",function(){return n}),i.d(t,"c",function(){return s}),i.d(t,"b",function(){return o});const r=e=>`https://github.com/home-assistant/home-assistant/issues?q=is%3Aissue+is%3Aopen+label%3A%22integration%3A+${e}%22`,n=(e,t)=>e(`component.${t}.title`)||t,s=e=>e.callWS({type:"manifest/list"}),o=(e,t)=>e.callWS({type:"manifest/get",integration:t})},429:function(e,t,i){"use strict";i(4);var r=i(75),n=i(5),s=i(3),o=i(65);Object(n.a)({is:"paper-icon-button-light",_template:s.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 24px;
        height: 24px;
      }

      paper-ripple {
        opacity: 0.6;
        color: currentColor;
        @apply --paper-icon-button-light-ripple;
      }

      :host > ::slotted(button) {
        position: relative;
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        background: none;
        border: none;
        outline: none;
        vertical-align: middle;
        color: inherit;
        cursor: pointer;
        /* NOTE: Both values are needed, since some phones require the value to be \`transparent\`. */
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-tap-highlight-color: transparent;
      }
      :host > ::slotted(button[disabled]) {
        color: #9b9b9b;
        pointer-events: none;
        cursor: auto;
      }
    </style>
    <slot></slot>
  `,behaviors:[r.a],registered:function(){this._template.setAttribute("strip-whitespace","")},ready:function(){Object(o.a)(this,()=>{this.addEventListener("down",this._rippleDown.bind(this)),this.addEventListener("up",this._rippleUp.bind(this));var e=this.getEffectiveChildren()[0];this._rippleContainer=e,e.addEventListener("focus",this._rippleDown.bind(this)),e.addEventListener("blur",this._rippleUp.bind(this))})},_rippleDown:function(){this.getRipple().uiDownAction()},_rippleUp:function(){this.getRipple().uiUpAction()},ensureRipple:function(e){var t=this._ripple;r.a.ensureRipple.apply(this,arguments),this._ripple&&this._ripple!==t&&(this._ripple.center=!0,this._ripple.classList.add("circle"))}})},895:function(e,t,i){"use strict";i.r(t);i(94),i(234),i(73),i(202);var r=i(0),n=(i(214),i(338)),s=i(44),o=i(11),a=i(132);const l=(e,t,i)=>{if(1!==t.length)return e[t[0]]||(e[t[0]]={}),l(e[t[0]],t.slice(1),i);e[t[0]]=i},c=(e,t)=>1===t.length?e[t[0]]:void 0!==e[t[0]]?c(e[t[0]],t.slice(1)):void 0;i(119),i(131),i(195),i(123),i(225);var d=i(134),p=i(210),h=i(249),u=i(230),f=i(252),v=i(281);i(429),i(340);function m(e){var t,i=_(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function b(e){return e.decorators&&e.decorators.length}function g(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function k(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function _(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!b(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=_(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=k(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=k(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var o=t(function(e){n.initializeInstanceElements(e,a.elements)},i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(g(s.descriptor)||g(n.descriptor)){if(b(s)||b(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(b(s)){if(b(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}y(s,n)}else t.push(s)}return t}(o.d.map(m)),e);n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([Object(r.d)("ha-devices-picker")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"value",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[Object(r.g)({attribute:"picked-device-label"}),Object(r.g)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",key:"pickedDeviceLabel",value:void 0},{kind:"field",decorators:[Object(r.g)({attribute:"pick-device-label"})],key:"pickDeviceLabel",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return r.f``;const e=this._currentDevices;return r.f`
      ${e.map(e=>r.f`
          <div>
            <ha-device-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .value=${e}
              .label=${this.pickedDeviceLabel}
              @value-changed=${this._deviceChanged}
            ></ha-device-picker>
          </div>
        `)}
      <div>
        <ha-device-picker
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .label=${this.pickDeviceLabel}
          @value-changed=${this._addDevice}
        ></ha-device-picker>
      </div>
    `}},{kind:"get",key:"_currentDevices",value:function(){return this.value||[]}},{kind:"method",key:"_updateDevices",value:async function(e){Object(o.a)(this,"value-changed",{value:e}),this.value=e}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;i!==t&&""===i&&(""===i?this._updateDevices(this._currentDevices.filter(e=>e!==t)):this._updateDevices(this._currentDevices.map(e=>e===t?i:e)))}},{kind:"method",key:"_addDevice",value:async function(e){e.stopPropagation();const t=e.detail.value;if(e.currentTarget.value="",!t)return;const i=this._currentDevices;i.includes(t)||this._updateDevices([...i,t])}}]}},r.a);function E(e){var t,i=j(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function O(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function D(e){return e.decorators&&e.decorators.length}function C(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function x(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function j(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function P(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function $(e,t,i){return($="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=A(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}})(e,t,i||e)}function A(e){return(A=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,i,r){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!D(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return P(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?P(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=j(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=x(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=x(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var o=t(function(e){n.initializeInstanceElements(e,a.elements)},i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(C(s.descriptor)||C(n.descriptor)){if(D(s)||D(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(D(s)){if(D(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}O(s,n)}else t.push(s)}return t}(o.d.map(E)),e);n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([Object(r.d)("ha-area-devices-picker")],function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"label",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"value",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"area",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"devices",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[Object(r.g)({type:Boolean})],key:"_opened",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_areaPicker",value:()=>!0},{kind:"field",decorators:[Object(r.g)()],key:"_devices",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_areas",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_entities",value:void 0},{kind:"field",key:"_selectedDevices",value:()=>[]},{kind:"field",key:"_filteredDevices",value:()=>[]},{kind:"field",key:"_getDevices",value(){return Object(d.a)((e,t,i,r,n,s)=>{if(!e.length)return[];const o={};for(const a of i)a.device_id&&(a.device_id in o||(o[a.device_id]=[]),o[a.device_id].push(a));let l=[...e];r&&(l=l.filter(e=>{const t=o[e.id];return!(!t||!t.length)&&o[e.id].some(e=>r.includes(Object(a.a)(e.entity_id)))})),n&&(l=l.filter(e=>{const t=o[e.id];return!t||!t.length||i.every(e=>!n.includes(Object(a.a)(e.entity_id)))})),s&&(l=l.filter(e=>{const t=o[e.id];return!(!t||!t.length)&&o[e.id].some(e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&s.includes(t.attributes.device_class))})})),this._filteredDevices=l;const c={};for(const a of t)c[a.area_id]=a;const d={};for(const a of l){const e=a.area_id;e&&(e in d||(d[e]={id:e,name:c[e].name,devices:[]}),d[e].devices.push(a.id))}return Object.keys(d).sort((e,t)=>Object(p.b)(d[e].name||"",d[t].name||"")).map(e=>d[e])})}},{kind:"method",key:"hassSubscribe",value:function(){return[Object(u.c)(this.hass.connection,e=>{this._devices=e}),Object(h.c)(this.hass.connection,e=>{this._areas=e}),Object(f.e)(this.hass.connection,e=>{this._entities=e})]}},{kind:"method",key:"updated",value:function(e){if($(A(i.prototype),"updated",this).call(this,e),e.has("area")&&this.area)this._areaPicker=!0,this.value=this.area;else if(e.has("devices")&&this.devices){this._areaPicker=!1;const e=this._filteredDevices.map(e=>e.id),t=this.devices.filter(t=>e.includes(t));this._setValue(t)}}},{kind:"method",key:"render",value:function(){if(!this._devices||!this._areas||!this._entities)return r.f``;const e=this._getDevices(this._devices,this._areas,this._entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses);return this._areaPicker&&0!==e.length?r.f`
      <vaadin-combo-box-light
        item-value-path="id"
        item-id-path="id"
        item-label-path="name"
        .items=${e}
        .value=${this._value}
        .renderer=${(e,t,i)=>{e.firstElementChild||(e.innerHTML="\n    <style>\n      paper-item {\n        width: 100%;\n        margin: -10px 0;\n        padding: 0;\n      }\n      paper-icon-button {\n        float: right;\n      }\n      .devices {\n        display: none;\n      }\n      .devices.visible {\n        display: block;\n      }\n    </style>\n    <paper-item>\n      <paper-item-body two-line=\"\">\n        <div class='name'>[[item.name]]</div>\n        <div secondary>[[item.devices.length]] devices</div>\n      </paper-item-body>\n    </paper-item>\n    "),e.querySelector(".name").textContent=i.item.name,e.querySelector("[secondary]").textContent=`${i.item.devices.length.toString()} devices`}}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._areaPicked}
      >
        <paper-input
          .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):`${this.label} in area`}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
        >
          ${this.value?r.f`
                <paper-icon-button
                  aria-label=${this.hass.localize("ui.components.device-picker.clear")}
                  slot="suffix"
                  class="clear-button"
                  icon="hass:close"
                  @click=${this._clearValue}
                  no-ripple
                >
                  Clear
                </paper-icon-button>
              `:""}
          ${e.length>0?r.f`
                <paper-icon-button
                  aria-label=${this.hass.localize("ui.components.device-picker.show_devices")}
                  slot="suffix"
                  class="toggle-button"
                  .icon=${this._opened?"hass:menu-up":"hass:menu-down"}
                >
                  Toggle
                </paper-icon-button>
              `:""}
        </paper-input>
      </vaadin-combo-box-light>
      <mwc-button @click=${this._switchPicker}
        >Choose individual devices</mwc-button
      >
    `:r.f`
        <ha-devices-picker
          @value-changed=${this._devicesPicked}
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .value=${this._selectedDevices}
          .pickDeviceLabel=${`Add ${this.label} device`}
          .pickedDeviceLabel=${`${this.label} device`}
        ></ha-devices-picker>
        ${e.length>0?r.f`
              <mwc-button @click=${this._switchPicker}
                >Choose an area</mwc-button
              >
            `:""}
      `}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),this._setValue([])}},{kind:"get",key:"_value",value:function(){return this.value||[]}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_switchPicker",value:async function(){this._areaPicker=!this._areaPicker}},{kind:"method",key:"_areaPicked",value:async function(e){const t=e.detail.value;let i=[];const r=e.target;r.selectedItem&&(i=r.selectedItem.devices),t===this._value&&this._selectedDevices===i||this._setValue(i,t)}},{kind:"method",key:"_devicesPicked",value:function(e){e.stopPropagation();const t=e.detail.value;this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e,t=""){this.value=t,this._selectedDevices=e,setTimeout(()=>{Object(o.a)(this,"value-changed",{value:e}),Object(o.a)(this,"change")},0)}},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      paper-input > paper-icon-button {
        width: 24px;
        height: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}]}},Object(v.a)(r.a));var T=i(250);i(201);function S(e){var t,i=L(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function z(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function I(e){return e.decorators&&e.decorators.length}function F(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function N(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function L(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function V(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!I(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return V(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?V(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=L(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=N(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=N(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var o=t(function(e){n.initializeInstanceElements(e,a.elements)},i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(F(s.descriptor)||F(n.descriptor)){if(I(s)||I(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(I(s)){if(I(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}z(s,n)}else t.push(s)}return t}(o.d.map(S)),e);n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([Object(r.d)("ha-thingtalk-placeholders")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"opened",value:void 0},{kind:"field",key:"skip",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"placeholders",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_error",value:void 0},{kind:"field",key:"_deviceEntityLookup",value:()=>({})},{kind:"field",decorators:[Object(r.g)()],key:"_extraInfo",value:()=>({})},{kind:"field",decorators:[Object(r.g)()],key:"_placeholderValues",value:()=>({})},{kind:"field",key:"_devices",value:void 0},{kind:"field",key:"_areas",value:void 0},{kind:"field",key:"_search",value:()=>!1},{kind:"method",key:"hassSubscribe",value:function(){return[Object(f.e)(this.hass.connection,e=>{for(const t of e)t.device_id&&(t.device_id in this._deviceEntityLookup||(this._deviceEntityLookup[t.device_id]=[]),this._deviceEntityLookup[t.device_id].includes(t.entity_id)||this._deviceEntityLookup[t.device_id].push(t.entity_id))}),Object(u.c)(this.hass.connection,e=>{this._devices=e,this._searchNames()}),Object(h.c)(this.hass.connection,e=>{this._areas=e,this._searchNames()})]}},{kind:"method",key:"updated",value:function(e){e.has("placeholders")&&(this._search=!0,this._searchNames())}},{kind:"method",key:"render",value:function(){return r.f`
      <ha-paper-dialog
        modal
        with-backdrop
        .opened=${this.opened}
        @opened-changed="${this._openedChanged}"
      >
        <h2>Great! Now we need to link some devices.</h2>
        <paper-dialog-scrollable>
          ${this._error?r.f` <div class="error">${this._error}</div> `:""}
          ${Object.entries(this.placeholders).map(([e,t])=>r.f`
                <h3>
                  ${this.hass.localize(`ui.panel.config.automation.editor.${e}s.name`)}:
                </h3>
                ${t.map(t=>{if(t.fields.includes("device_id")){const i=c(this._extraInfo,[e,t.index]);return r.f`
                      <ha-area-devices-picker
                        .type=${e}
                        .placeholder=${t}
                        @value-changed=${this._devicePicked}
                        .hass=${this.hass}
                        .area=${i?i.area_id:void 0}
                        .devices=${i&&i.device_ids?i.device_ids:void 0}
                        .includeDomains=${t.domains}
                        .includeDeviceClasses=${t.device_classes}
                        .label=${this._getLabel(t.domains,t.device_classes)}
                      ></ha-area-devices-picker>
                      ${i&&i.manualEntity?r.f`
                            <h3>
                              One or more devices have more than one matching
                              entity, please pick the one you want to use.
                            </h3>
                            ${Object.keys(i.manualEntity).map(i=>r.f`
                                <ha-entity-picker
                                  id="device-entity-picker"
                                  .type=${e}
                                  .placeholder=${t}
                                  .index=${i}
                                  @change=${this._entityPicked}
                                  .includeDomains=${t.domains}
                                  .includeDeviceClasses=${t.device_classes}
                                  .hass=${this.hass}
                                  .label=${`${this._getLabel(t.domains,t.device_classes)} of device ${this._getDeviceName(c(this._placeholderValues,[e,t.index,i,"device_id"]))}`}
                                  .entityFilter=${r=>{const n=this._placeholderValues[e][t.index][i].device_id;return this._deviceEntityLookup[n].includes(r.entity_id)}}
                                ></ha-entity-picker>
                              `)}
                          `:""}
                    `}return t.fields.includes("entity_id")?r.f`
                      <ha-entity-picker
                        .type=${e}
                        .placeholder=${t}
                        @change=${this._entityPicked}
                        .includeDomains=${t.domains}
                        .includeDeviceClasses=${t.device_classes}
                        .hass=${this.hass}
                        .label=${this._getLabel(t.domains,t.device_classes)}
                      ></ha-entity-picker>
                    `:r.f`
                    <div class="error">
                      Unknown placeholder<br />
                      ${t.domains}<br />
                      ${t.fields.map(e=>r.f` ${e}<br /> `)}
                    </div>
                  `})}
              `)}
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <mwc-button class="left" @click="${this.skip}">
            Skip
          </mwc-button>
          <mwc-button @click="${this._done}" .disabled=${!this._isDone}>
            Create automation
          </mwc-button>
        </div>
      </ha-paper-dialog>
    `}},{kind:"method",key:"_getDeviceName",value:function(e){if(!this._devices)return"";const t=this._devices.find(t=>t.id===e);return t&&(t.name_by_user||t.name)||""}},{kind:"method",key:"_searchNames",value:function(){this._search&&this._areas&&this._devices&&(this._search=!1,Object.entries(this.placeholders).forEach(([e,t])=>t.forEach(t=>{if(!t.name)return;const i=t.name,r=this._areas.find(e=>e.name.toLowerCase().includes(i));if(r)return l(this._extraInfo,[e,t.index,"area_id"],r.area_id),void this.requestUpdate("_extraInfo");const n=this._devices.filter(e=>{const t=e.name_by_user||e.name;return!!t&&t.toLowerCase().includes(i)});n.length&&(l(this._extraInfo,[e,t.index,"device_ids"],n.map(e=>e.id)),this.requestUpdate("_extraInfo"))})))}},{kind:"get",key:"_isDone",value:function(){return Object.entries(this.placeholders).every(([e,t])=>t.every(t=>t.fields.every(i=>{const r=c(this._placeholderValues,[e,t.index]);return!!r&&Object.values(r).every(e=>void 0!==e[i]&&""!==e[i])})))}},{kind:"method",key:"_getLabel",value:function(e,t){return`${e.map(e=>Object(T.a)(this.hass.localize,e)).join(", ")}${t?` of type ${t.join(", ")}`:""}`}},{kind:"method",key:"_devicePicked",value:function(e){const t=e.detail.value;if(!t)return;const i=e.target,r=i.placeholder,n=i.type;let s=c(this._placeholderValues,[n,r.index]);s&&(s=Object.values(s));const d=c(this._extraInfo,[n,r.index]);this._placeholderValues[n]&&delete this._placeholderValues[n][r.index],this._extraInfo[n]&&delete this._extraInfo[n][r.index],t.length?(t.forEach((e,t)=>{let i;if(s){const o=s.find((t,r)=>(i=r,t.device_id===e));if(o)return l(this._placeholderValues,[n,r.index,t],o),void(d&&l(this._extraInfo,[n,r.index,t],d[i]))}if(l(this._placeholderValues,[n,r.index,t,"device_id"],e),!r.fields.includes("entity_id"))return;const o=this._deviceEntityLookup[e].filter(e=>{if(r.device_classes){const t=this.hass.states[e];return!!t&&(r.domains.includes(Object(a.a)(e))&&t.attributes.device_class&&r.device_classes.includes(t.attributes.device_class))}return r.domains.includes(Object(a.a)(e))});0===o.length?this._error=`No ${r.domains.map(e=>Object(T.a)(this.hass.localize,e)).join(", ")} entities found in this device.`:1===o.length?(l(this._placeholderValues,[n,r.index,t,"entity_id"],o[0]),this.requestUpdate("_placeholderValues")):(delete this._placeholderValues[n][r.index][t].entity_id,l(this._extraInfo,[n,r.index,"manualEntity",t],!0),this.requestUpdate("_placeholderValues"))}),Object(o.a)(this.shadowRoot.querySelector("ha-paper-dialog"),"iron-resize")):this.requestUpdate("_placeholderValues")}},{kind:"method",key:"_entityPicked",value:function(e){const t=e.target,i=t.placeholder,r=t.value,n=t.type,s=t.index||0;l(this._placeholderValues,[n,i.index,s,"entity_id"],r),this.requestUpdate("_placeholderValues")}},{kind:"method",key:"_done",value:function(){Object(o.a)(this,"placeholders-filled",{value:this._placeholderValues})}},{kind:"method",key:"_openedChanged",value:function(e){this.dispatchEvent(new CustomEvent(e.type,e))}},{kind:"get",static:!0,key:"styles",value:function(){return[s.c,r.c`
        ha-paper-dialog {
          max-width: 500px;
        }
        mwc-button.left {
          margin-right: auto;
        }
        paper-dialog-scrollable {
          margin-top: 10px;
        }
        h3 {
          margin: 10px 0 0 0;
          font-weight: 500;
        }
        .error {
          color: var(--google-red-500);
        }
      `]}}]}},Object(v.a)(r.a));function R(e){var t,i=H(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function U(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function B(e){return e.decorators&&e.decorators.length}function q(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function K(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function H(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function M(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,n)},this),e.forEach(function(e){if(!B(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return M(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(i):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?M(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=H(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=K(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=K(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var o=t(function(e){n.initializeInstanceElements(e,a.elements)},i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(q(s.descriptor)||q(n.descriptor)){if(B(s)||B(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(B(s)){if(B(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}U(s,n)}else t.push(s)}return t}(o.d.map(R)),e);n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([Object(r.d)("ha-dialog-thinktalk")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(r.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_error",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_params",value:void 0},{kind:"field",decorators:[Object(r.g)()],key:"_submitting",value:()=>!1},{kind:"field",decorators:[Object(r.g)()],key:"_opened",value:()=>!1},{kind:"field",decorators:[Object(r.g)()],key:"_placeholders",value:void 0},{kind:"field",decorators:[Object(r.h)("#input")],key:"_input",value:void 0},{kind:"field",key:"_value",value:void 0},{kind:"field",key:"_config",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._error=void 0,this._opened=!0}},{kind:"method",key:"render",value:function(){return this._params?this._placeholders?r.f`
        <ha-thingtalk-placeholders
          .hass=${this.hass}
          .placeholders=${this._placeholders}
          .opened=${this._opened}
          .skip=${()=>this._skip()}
          @opened-changed=${this._openedChanged}
          @placeholders-filled=${this._handlePlaceholders}
        >
        </ha-thingtalk-placeholders>
      `:r.f`
      <ha-paper-dialog
        with-backdrop
        .opened=${this._opened}
        @opened-changed=${this._openedChanged}
      >
        <h2>Create a new automation</h2>
        <paper-dialog-scrollable>
          ${this._error?r.f` <div class="error">${this._error}</div> `:""}
          Type below what this automation should do, and we will try to convert
          it into a Home Assistant automation. (only English is supported for
          now)<br /><br />
          For example:
          <ul @click=${this._handleExampleClick}>
            <li>
              <button class="link">
                Turn off the lights when I leave home
              </button>
            </li>
            <li>
              <button class="link">
                Turn on the lights when the sun is set
              </button>
            </li>
            <li>
              <button class="link">
                Notify me if the door opens and I am not at home
              </button>
            </li>
            <li>
              <button class="link">
                Turn the light on when motion is detected
              </button>
            </li>
          </ul>
          <paper-input
            id="input"
            label="What should this automation do?"
            autofocus
            @keyup=${this._handleKeyUp}
          ></paper-input>
          <a
            href="https://almond.stanford.edu/"
            target="_blank"
            rel="noreferrer"
            class="attribution"
            >Powered by Almond</a
          >
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <mwc-button class="left" @click="${this._skip}">
            Skip
          </mwc-button>
          <mwc-button @click="${this._generate}" .disabled=${this._submitting}>
            <paper-spinner
              ?active="${this._submitting}"
              alt="Creating your automation..."
            ></paper-spinner>
            Create automation
          </mwc-button>
        </div>
      </ha-paper-dialog>
    `:r.f``}},{kind:"method",key:"_generate",value:async function(){if(this._value=this._input.value,!this._value)return void(this._error="Enter a command or tap skip.");let e,t;this._submitting=!0;try{const r=await Object(n.c)(this.hass,this._value);e=r.config,t=r.placeholders}catch(i){return this._error=i.message,void(this._submitting=!1)}this._submitting=!1,Object.keys(e).length?Object.keys(t).length?(this._config=e,this._placeholders=t):this._sendConfig(this._value,e):this._error="We couldn't create an automation for that (yet?)."}},{kind:"method",key:"_handlePlaceholders",value:function(e){const t=e.detail.value;Object.entries(t).forEach(([e,t])=>{Object.entries(t).forEach(([t,i])=>{const r=Object.values(i);if(1===r.length)return void Object.entries(r[0]).forEach(([i,r])=>{this._config[e][t][i]=r});const n=Object.assign({},this._config[e][t]),s=[];r.forEach(e=>{const t=Object.assign({},n);Object.entries(e).forEach(([e,i])=>{t[e]=i}),s.push(t)}),this._config[e].splice(t,1,...s)})}),this._sendConfig(this._value,this._config)}},{kind:"method",key:"_sendConfig",value:function(e,t){this._params.callback(Object.assign({alias:e},t)),this._closeDialog()}},{kind:"method",key:"_skip",value:function(){this._params.callback(void 0),this._closeDialog()}},{kind:"method",key:"_closeDialog",value:function(){this._placeholders=void 0,this._input&&(this._input.value=null),this._opened=!1}},{kind:"method",key:"_openedChanged",value:function(e){e.detail.value||this._closeDialog()}},{kind:"method",key:"_handleKeyUp",value:function(e){13===e.keyCode&&this._generate()}},{kind:"method",key:"_handleExampleClick",value:function(e){this._input.value=e.target.innerText}},{kind:"get",static:!0,key:"styles",value:function(){return[s.b,s.c,r.c`
        ha-paper-dialog {
          max-width: 500px;
        }
        mwc-button.left {
          margin-right: auto;
        }
        mwc-button paper-spinner {
          width: 14px;
          height: 14px;
          margin-right: 20px;
        }
        paper-spinner {
          display: none;
        }
        paper-spinner[active] {
          display: block;
        }
        .error {
          color: var(--google-red-500);
        }
        .attribution {
          color: var(--secondary-text-color);
        }
      `]}}]}},r.a)}}]);
//# sourceMappingURL=chunk.8a77bebdcfb11c7735aa.js.map