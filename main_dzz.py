from myclass import Cards, Player, PlayRecords, WebShow
from myutil import game_init
import json
import time
import copy                   
class Game(object):
    
    def __init__(self, model):
        #初始化一副扑克牌类
        self.cards = Cards()
        
        #play相关参数
        self.end = False
        self.last_move_type = self.last_move = "start"
        self.playround = 1

        self.yaobuqis = []

        #choose模型
        self.model = model
        self.t = (input('是否当地主:'))
        if self.t=='Y':
            self.i=2
            print('您已成为地主')
        elif self.t=='N':
             self.i=0
             print('player1已成为地主')
        else: print('选择错误，请重新开始游戏')



    #发牌
    def game_start(self):
        
        #初始化players
        self.players = []
        for i in range(1,4):
            self.players.append(Player(1))
            self.players.append(Player(2))
            self.players.append(Player('玩家'))

        #初始化扑克牌记录类
        self.playrecords = PlayRecords()    

        #发牌
        game_init(self.players, self.playrecords, self.cards,self.i)
    
    
    #返回扑克牌记录类
    def get_record(self):
        web_show = WebShow(self.playrecords)
        return json.encode(web_show, unpicklable=False)
        
    #游戏进行    
    def next_move(self):
        
        self.last_move_type, self.last_move, self.end, self.yaobuqi = self.players[self.i].go(self.last_move_type, 
                                                            self.last_move, self.playrecords, self.model)
        if self.yaobuqi:
            self.yaobuqis.append(self.i)
        else:
            self.yaobuqis = []
        #都要不起
        if len(self.yaobuqis) == 2:
            self.yaobuqis = []
            self.last_move_type = self.last_move = "start"
        if self.end:
            self.playrecords.winner = self.i+1
        self.i = self.i + 1
        #一轮结束
        if self.i > 2:
            #self.playrecords.show("=============Round " + str(self.playround) + " End=============")
            self.playround = self.playround + 1
            #self.playrecords.show("=============Round " + str(self.playround) + " Start=============")
            self.i = 0    
        
   
if __name__=="__main__":
    
    begin = time.time()
    game_ddz = Game("random")
    game_ddz.game_start()

    for j in range(1):
        #game_ddz = copy.deepcopy(game_ddz)
        i = 0
        while(game_ddz.playrecords.winner == 0):
            game_ddz.playrecords.show(str(i))
            game_ddz.next_move()
            i = i + 1
            if game_ddz.playrecords.winner==3:
               game_ddz.playrecords.winner= '玩家'
        print('本轮比赛的获胜者是：','Player'+str(game_ddz.playrecords.winner))
    print('游戏总时长为',str(time.time()-begin)+'s')
