<?php

// Initially set a static file name, could be read from .env
$static_fileName = "instructions.pdf";
function getData($key, $value){
    $safeKey = htmlspecialchars($key);
    $safeValue = htmlspecialchars($value);

    $postData = array(
        'title' => 'blog',
        'author' => 'Admin',
        $safeKey => $safeValue,
    );
    return $postData;
}

$blogData = getData($_GET['key'], $_GET['value']);

extract($blogData);

echo "hello " . $firstName;
// The file specified in $static_fileName is included.
include($static_fileName);
?>
