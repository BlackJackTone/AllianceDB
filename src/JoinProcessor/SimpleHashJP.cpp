//
// Created by tony on 2022/2/8.
//

#include <JoinProcessor/SimpleHashJP.h>
using namespace INTELLI;
using namespace std;
void INTELLI::SimpleHashJP::inlineRun() {
  //first bind to the core
  UtilityFunctions::bind2Core(cpuBind);
  //wait for new cmd
  //cout<<"join processor "<<sysId<<" start"<<endl;
  while (1) {
    /*while (cmdQueueIn->empty()&&tupleQueueS->empty()&&tupleQueueR->) {

    }*/
    //cmd
    if (tupleQueueS->empty() && tupleQueueR->empty()) {
      if (!cmdQueueIn->empty()) {

        join_cmd_t cmdIn = *cmdQueueIn->front();
        cmdQueueIn->pop();
        if (cmdIn == CMD_STOP) {
          sendAck();
          cout << "join processor " << sysId << " end" << endl;
          return;
        }
      }

    }


    //tuple S and window R
    while (!tupleQueueS->empty()) {
      TuplePtr ts = *tupleQueueS->front();
      tupleQueueS->pop();
      WindowOfTuples wr = *windowQueueR->front();
      windowQueueR->pop();
      //build R
      size_t rSize = wr.size();
     hashtable hashtableR;
      for (size_t i = 0; i < rSize; i++) {
        TuplePtr tr = wr[i];
        hashtableR.emplace(tr->key, 0, tr->subKey);
      }
      //probe S
      auto findMatchR = hashtableR.find(ts->key);
      if (findMatchR != hashtableR.end()) {
        size_t matches = findMatchR->second.size();
        joinedResult += matches;
        //printf("JP%ld:S[%ld](%ld) find %ld R matches\r\n", sysId, ts->subKey + 1, ts->key, matches);
      }
      /*for (size_t i = 0; i < rSize; i++) {
        TuplePtr tr=wr[i];
        if(tr->key==ts->key)
        {
          joinedResult++;
        }
      }*/
    }

    //tuple R and window S
    while (!tupleQueueR->empty()) {
      TuplePtr tr = *tupleQueueR->front();
      tupleQueueR->pop();
      WindowOfTuples ws = *windowQueueS->front();
      windowQueueS->pop();
      //build S
      size_t sSize = ws.size();
      hashtable hashtableS;
      for (size_t i = 0; i < sSize; i++) {
        TuplePtr ts = ws[i];
        hashtableS.emplace(ts->key, 0, ts->subKey);
      }
      //probe R
      auto findMatchS = hashtableS.find(tr->key);
      if (findMatchS != hashtableS.end()) {
        size_t matches = findMatchS->second.size();
        joinedResult += matches;
        // printf("JP%ld:R[%ld](%ld) find %ld S matches\r\n", sysId, tr->subKey + 1, tr->key, matches);
      }
     /* for (size_t i = 0; i < sSize; i++) {
        TuplePtr ts=ws[i];
        if(tr->key==ts->key)
        {
          joinedResult++;
        }
      }*/
    }
  }
}