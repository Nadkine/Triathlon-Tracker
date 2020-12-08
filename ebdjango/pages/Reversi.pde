import java.util.ArrayList;
import java.util.List;
import processing.core.*;

 int scoreBlack;
  int scoreWhite;
  List<Square> potentialSquares = new ArrayList();
  boolean bool = false;
  int count = 0;
  Square previousSquare;
  Square currentSquare;
  Square[][] board;
  Player blackPlayer;
  Player whitePlayer;
  boolean whiteTurn = true;
  
  float w;
  
  public void setup() { 
    size(600,600);
    board = new Square[8][8];
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        board[i][j] = new Square(i,j);
      }
    }
    w = height/8;
    board[3][4].containsBlack = true;
    board[4][3].containsBlack = true;
    board[3][3].containsWhite = true;
    board[4][4].containsWhite = true;
    previousSquare = board[0][0];
     checkScore();
    
  }
  
  public void draw() {
    background(70,200,90);
                fill(0);
    renderBoard(board);
                fill(255,50,50);
                textSize(50);
                strokeWeight(5);
                textMode(CENTER);
                text(scoreWhite,50,50);
                text(scoreBlack,width-80,50);
               
  }
  
  public void renderBoard(Square[][] board) {
    for (int i = 0; i < board.length; i++) {
      for (int j = 0; j < board[i].length; j++) {
        board[i][j].drawSquare();
      }
    }
  }
  
  void mouseMoved() {
      currentSquare = board[floor(mouseX/w)][floor(mouseY/w)];
      if (previousSquare != currentSquare){
          previousSquare.showBlack = false;
          previousSquare.showWhite = false;

          if (checkAvailability(currentSquare, whiteTurn)) {
                  if (whiteTurn) {
                      currentSquare.showWhite = true;
                  } else {
                      currentSquare.showBlack = true;
                  }
          }
          previousSquare = currentSquare;
      }
  }
        
  void mousePressed() {
    currentSquare = board[floor(mouseX/w)][floor(mouseY/w)];
    if (!currentSquare.containsBlack && !currentSquare.containsWhite) {
                    if (checkAvailability(currentSquare, whiteTurn)) {
                        if (whiteTurn) {
                                currentSquare.containsWhite = true;
                        } else {
                                currentSquare.containsBlack = true;
                        }
                        changeSquares();
                        checkScore();
                        if (checkTurnPossible()){
                        whiteTurn = !whiteTurn;
                        } 
                    }                                      
    }  
  }
  
  public boolean checkAvailability(Square square, boolean whiteTurn) {
            boolean availability = false; 
            potentialSquares.clear();
            for (int i = -1; i <= 1; i++) {
                for (int j = -1; j <= 1; j++) {
                    int checkingI = square.i + i;
                    int checkingJ = square.j + j;
                    if (checkingI >= 0 && checkingJ >= 0 && checkingI <= 7 && checkingJ <= 7) {
                        Square checkSquare = board[checkingI][checkingJ];
                        if (whiteTurn && checkSquare!=currentSquare && checkSquare.containsBlack && checkRow(checkSquare,i, j,whiteTurn)){
                            potentialSquares.add(checkSquare);
                            availability = true;
                        }
                        else if (!whiteTurn && checkSquare!=currentSquare && checkSquare.containsWhite && checkRow(checkSquare,i, j,whiteTurn)){ 
                            potentialSquares.add(checkSquare);
                            availability = true;
                        }
                    }
                }
            }
            return availability;
  }
  
  private boolean checkRow(Square square, int i, int j, boolean whiteTurn) {
            List<Square> checkedSquares = new ArrayList();
            checkedSquares.clear();
            int checkingI = square.i + i;
            int checkingJ = square.j + j;
            while(checkingI >= 0 && checkingJ >= 0 && checkingI <= 7 && checkingJ <= 7) { 
                if(whiteTurn && board[checkingI][checkingJ].containsWhite) {
                    potentialSquares.addAll(checkedSquares);       
                    checkedSquares.clear();
                    return true;
                } else if(whiteTurn && board[checkingI][checkingJ].containsBlack) {
                    checkedSquares.add(board[checkingI][checkingJ]);   
                    checkingI += i;
                    checkingJ += j;
                } else if(!whiteTurn && board[checkingI][checkingJ].containsBlack) {
                    potentialSquares.addAll(checkedSquares);
                    checkedSquares.clear();
                    return true;
                } else if(!whiteTurn && board[checkingI][checkingJ].containsWhite) {
                    checkedSquares.add(board[checkingI][checkingJ]); 
                    checkingI += i;
                    checkingJ += j;
                } else {  
                    checkedSquares.clear();
                    return false;
                }
            }
             checkedSquares.clear();
            return false;
  }

    private void changeSquares() {
        for (Square square: potentialSquares){
            if (!whiteTurn){
                square.containsWhite = false;
                square.containsBlack = true;
            } else if (whiteTurn){
                square.containsBlack = false;
                square.containsWhite = true;
            }
        }
        potentialSquares.clear();
    }

    private void checkScore() {
        scoreWhite = scoreBlack = 0;
        for (int i = 0; i < board.length; i++) {
            for (int j = 0; j < board[i].length; j++) {
                if (board[i][j].containsBlack){
                    scoreBlack++;
                }
                if (board[i][j].containsWhite){
                    scoreWhite++;
                }
            }
        }
    }
    
    private boolean checkTurnPossible(){
        //for (int i = 0; i < board.length; i++) {
        //    for (int j = 0; j < board[i].length; j++) {
        //      //if (checkAvailability(board[i][j], whiteTurn)){
        //          System.out.println(true);
        //          return true;
        //      //}
        //    }
        //}        
        //System.out.println(false);
        return true;
    }


  
  class Player{
    

    boolean isMoving;
    
    public Player() {
      this.isMoving = false;
    }
    
  }
  
  class Square{
    
    float width = w;
    int i;
    int j;
    boolean containsBlack = false;
    boolean containsWhite = false;
    boolean showWhite = false;
    boolean showBlack = false;
    
    public Square(int i, int j) {
      this.i = i;
      this.j = j;
    }
    
    public void drawSquare() {
      noFill();
      strokeWeight(2);
      rect(i*w,j*w,w,w);
      strokeWeight(2);
      if(containsBlack || showBlack && !containsWhite) {
        fill(0);
        ellipse(i*w+0.5f*w,j*w+0.5f*w,w-5,w-5);
      }
      else if(containsWhite || showWhite) {
        fill(255);
        ellipse(i*w+0.5f*w,j*w+0.5f*w,w-5,w-5);
      } 
    }
  }
  
