(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[4016],{4016:(n,e,t)=>{"use strict";t.r(e);t.d(e,{Signal:()=>c});var r=t(93269);var i=t.n(r);var c=function(){function n(n){this.sender=n}n.prototype.connect=function(n,e){return o.connect(this,n,e)};n.prototype.disconnect=function(n,e){return o.disconnect(this,n,e)};n.prototype.emit=function(n){o.emit(this,n)};return n}();(function(n){function e(n,e){o.disconnectBetween(n,e)}n.disconnectBetween=e;function t(n){o.disconnectSender(n)}n.disconnectSender=t;function r(n){o.disconnectReceiver(n)}n.disconnectReceiver=r;function i(n){o.disconnectAll(n)}n.disconnectAll=i;function c(n){o.disconnectAll(n)}n.clearData=c;function a(){return o.exceptionHandler}n.getExceptionHandler=a;function u(n){var e=o.exceptionHandler;o.exceptionHandler=n;return e}n.setExceptionHandler=u})(c||(c={}));var o;(function(n){n.exceptionHandler=function(n){console.error(n)};function e(n,e,t){t=t||undefined;var r=s.get(n.sender);if(!r){r=[];s.set(n.sender,r)}if(g(r,n,e,t)){return false}var i=t||e;var c=l.get(i);if(!c){c=[];l.set(i,c)}var o={signal:n,slot:e,thisArg:t};r.push(o);c.push(o);return true}n.connect=e;function t(n,e,t){t=t||undefined;var r=s.get(n.sender);if(!r||r.length===0){return false}var i=g(r,n,e,t);if(!i){return false}var c=t||e;var o=l.get(c);i.signal=null;p(r);p(o);return true}n.disconnect=t;function i(n,e){var t=s.get(n);if(!t||t.length===0){return}var i=l.get(e);if(!i||i.length===0){return}(0,r.each)(i,(function(e){if(!e.signal){return}if(e.signal.sender===n){e.signal=null}}));p(t);p(i)}n.disconnectBetween=i;function c(n){var e=s.get(n);if(!e||e.length===0){return}(0,r.each)(e,(function(n){if(!n.signal){return}var e=n.thisArg||n.slot;n.signal=null;p(l.get(e))}));p(e)}n.disconnectSender=c;function o(n){var e=l.get(n);if(!e||e.length===0){return}(0,r.each)(e,(function(n){if(!n.signal){return}var e=n.signal.sender;n.signal=null;p(s.get(e))}));p(e)}n.disconnectReceiver=o;function a(n){c(n);o(n)}n.disconnectAll=a;function u(n,e){var t=s.get(n.sender);if(!t||t.length===0){return}for(var r=0,i=t.length;r<i;++r){var c=t[r];if(c.signal===n){v(c,e)}}}n.emit=u;var s=new WeakMap;var l=new WeakMap;var f=new Set;var d=function(){var n=typeof requestAnimationFrame==="function";return n?requestAnimationFrame:setImmediate}();function g(n,e,t,i){return(0,r.find)(n,(function(n){return n.signal===e&&n.slot===t&&n.thisArg===i}))}function v(e,t){var r=e.signal,i=e.slot,c=e.thisArg;try{i.call(c,r.sender,t)}catch(o){n.exceptionHandler(o)}}function p(n){if(f.size===0){d(h)}f.add(n)}function h(){f.forEach(A);f.clear()}function A(n){r.ArrayExt.removeAllWhere(n,m)}function m(n){return n.signal===null}})(o||(o={}))}}]);