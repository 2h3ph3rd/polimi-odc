<?php

class User
{
    public $name;
    public $id;
    public $isAdmin;
    public $solved;
    public $points;

    function __construct($id, $name)
    {
        $this->id = $id;
        $this->name = $name;
        $this->isAdmin = false;
        $this->solved = array();
        $this->points = 0;
    }

    function setSolved($challid)
    {
        array_push($this->solved, $challid);
    }
}

class Challenge
{
    //WIP Not used yet.
    public $name;
    public $description;
    public $setup_cmd = NULL;
    // public $check_cmd=NULL;
    public $stop_cmd = NULL;

    function __construct($name, $description, $stop_cmd)
    {
        $this->name = $name;
        $this->description = $description;
        $this->stop_cmd = $stop_cmd;
    }

    function start()
    {
        if (!is_null($this->setup_cmd)) {
            $output = null;
            $retval = null;
            echo ("Starting challenge!");
            exec($this->setup_cmd, $output, $retval);
            echo ($output[0]);
        }
    }

    function stop()
    {
        if (!is_null($this->stop_cmd)) {
            $output = null;
            $retval = null;
            echo ("Stoping challenge!");
            exec($this->stop_cmd, $output, $retval);
            echo ($output[0]);
        }
    }


    function __destruct()
    {
        $this->stop();
    }

}

$challenge = new Challenge("A", "B", "cat /flag.txt");
$user = new User($challenge, "1337");
print(serialize($user));
?>