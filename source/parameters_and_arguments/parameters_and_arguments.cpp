#pragma once

/*
This example demonstrates how to configure line breaks in long parameter and
argument lists. There are two common ways to do this:
- Brace aligned.
- All single indented.
- Some single indented.

Brace aligned:
void myFunction(firstParameter, secondParameter,
                thirdParameter);


All signle indented:
void myFunction(
  firstParameter, secondParameter, thirdParameter);


Some single indented:
void myFunction(firstParameter,
  secondParameter, thirdParameter)
*/



/*
Helpers.
*/

class MyClass;

namespace MyClassHelpers
{
  struct MyClassParticipant
  {
    MyClassParticipant(MyClass& participant);
    MyClass& m_participant;
  };
}



/*
Very long lines.

Variant where we start with no extra line breaks.
*/


// Very long lines: class definition.
class MyClassA
{
  public:
    MyClassA(MyClassA& firstParticipant, MyClassA& secondParticipant);
    MyClassA(MyClassHelpers::MyClassParticipant firstParticipant, MyClassHelpers::MyClassParticipant secondParticipant);

    void performRecursiveParticipantProcessing(MyClassA& firstParticipant, MyClassA&secondParticipant);
    void performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant& firstParticipant, MyClassHelpers::MyClassParticipant& secondParticipant);

  private:
    MyClassHelpers::MyClassParticipant m_firstParticipant;
    MyClassHelpers::MyClassParticipant m_secondParticipant;
};



// Very long lines: constructor 1 definition.
MyClassA::MyClassA(MyClassA& firstParticipant, MyClassA& secondParticipant) : MyClassA(MyClassHelpers::MyClassParticipant(firstParticipant), MyClassHelpers::MyClassParticipant(secondParticipant))
{
}

// Very long lines: constructor 2 definition.
MyClassA:: MyClassA(MyClassHelpers::MyClassParticipant fistParticipant, MyClassHelpers::MyClassParticipant secondParticipant) : m_firstParticipant(m_firstParticipant), m_secondParticipant(secondParticipant)
{
}

// Very long lines: member function 1 definition.
void MyClassA::performRecursiveParticipantProcessing(MyClassA& firstParticipant, MyClassA& secondParticipant)
{
  m_firstParticipant.performRecursiveParticipantProcessing(m_firstParticipant.m_participant, m_secondParticipant.m_participant);
}


// Very long lines: member function 2 definition.
void MyClassA::performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant& firstParticipant, MyClassHelpers::MyClassParticipant& secondParticipant)
{
  m_firstParticipant.m_participant.performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant(m_firstParticipant.m_participant.m_firstParticipant.m_participant), MyClassHelpers::MyClassParticipant(m_firstParticipant.m_participant.m_secondParticipant.m_participant));
  m_secondParticipant.m_participant.performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant(m_secondParticipant.m_participant.m_firstParticipant.m_participant), MyClassHelpers::MyClassParticipant(m_secondParticipant.m_participant.m_secondParticipant.m_participant));
}



/*
Line break in lists, no '(' aligning.

Variant where we start with as many parameters as we can fit on the same line
as the opening '(' and then intent the continuation lines ones.
*/

// Line break in lists, no '(' aligning: class definition.
class MyClassB
{
  public:
    MyClassB(MyClassB& firstParticipant, MyClassB& secondParticipant);
    MyClassB(MyClassHelpers::MyClassParticipant firstParticipant,
      MyClassHelpers::MyClassParticipant secondParticipant);

    void performRecursiveParticipantProcessing(MyClassB& firstParticipant, MyClassB&secondParticipant);
    void performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant& firstParticipant,
      MyClassHelpers::MyClassParticipant& secondParticipant);

  private:
    MyClassHelpers::MyClassParticipant m_participant1;
    MyClassHelpers::MyClassParticipant m_participant2;
};


// Line break in lists, no '(' aligning: constructor 1 definition.
MyClassB::MyClassB(MyClassB& firstParticipant, MyClassB& secondParticipant) :
  MyClassB(MyClassHelpers::MyClassParticipant(firstParticipant),
    MyClassHelpers::MyClassParticipant(secondParticipant))
{
}

// Line break in lists, no '(' aligning: constructor 2 definition.
MyClassB:: MyClassB(MyClassHelpers::MyClassParticipant fistParticipant,
  MyClassHelpers::MyClassParticipant secondParticipant) :
    m_firstParticipant(m_firstParticipant),
    m_secondParticipant(secondParticipant)
{
}


// Line break in lists, no '(' aligning: member function 1 definition.
void MyClassB::performRecursiveParticipantProcessing(MyClassB& firstParticipant, MyClassB&secondParticipant)
{
  m_firstParticipant.performRecursiveParticipantProcessing(m_firstParticipant.m_participant,
    m_secondParticipant.m_participant);
}


// Line break in lists, no '(' aligning: Member function 2 definition.
void MyClassB::performRecursiveParticipantProcessing(MyClassHelpers:: MyClassParticipant& firstParticipant,
  MyClassHelpers::MyClassParticipant& secondParticipant)
{
  m_firstParticipant.m_participant.performRecursiveParticipantProcessing(
    MyClassHelpers::MyClassParticipant(m_firstParticipant.m_participant.m_firstParticipant.m_participant),
    MyClassHelpers::MyClassParticipant(m_firstParticipant.m_participant.m_secondParticipant.m_participant));
  m_secondParticipant.m_participant.performRecursiveParticipantProcessing(
    MyClassHelpers::MyClassParticipant(m_secondParticipant.m_participant.m_firstParticipant.m_participant),
    MyClassHelpers::MyClassParticipant(m_secondParticipant.m_participant.m_secondParticipant.m_participant));
}



/*
Line break in lists, with '(' aligning.
*/

// Line break in lists, with '(' aligning: Class definition.
class MyClassC
{
  public:
    MyClassC(MyClassC& firstParticipant, MyClassC& secondParticipant);
    MyClassC(MyClassHelpers::MyClassParticipant firstParticipant,
      MyClassHelpers::MyClassParticipant secondParticipant);

    void performRecursiveParticipantProcessing(MyClassC& firstParticipant, MyClassC&secondParticipant);
    void performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant& firstParticipant,
                                               MyClassHelpers::MyClassParticipant& secondParticipant);

  private:
    MyClassHelpers::MyClassParticipant m_participant1;
    MyClassHelpers::MyClassParticipant m_participant2;
};


// Line break in lists, with '(' aligning: Constructor 1 definition.
MyClassC::MyClassC(MyClassC& firstParticipant, MyClassC& secondParticipant) :
  MyClassC(MyClassHelpers::MyClassParticipant(firstParticipant),
          MyClassHelpers::MyClassParticipant(secondParticipant))
{
}

// Line break in lists, with '(' aligning: Constructor 2 definition.
MyClassC:: MyClassC(MyClassHelpers::MyClassParticipant fistParticipant,
                  MyClassHelpers::MyClassParticipant secondParticipant) :
  m_firstParticipant(m_firstParticipant), m_secondParticipant(secondParticipant)
{
}

// Line break in lists, with '(' aligning: member function 1 definition.
void MyClassC::performRecursiveParticipantProcessing(MyClassC& firstParticipant, MyClassC&secondParticipant)
{
  m_firstParticipant.performRecursiveParticipantProcessing(m_firstParticipant.m_participant,
                                                           m_secondParticipant.m_participant);
}


// Line break in lists, with '(' aligning: Member function 2 definition.
void MyClassC::performRecursiveParticipantProcessing(MyClassHelpers:: MyClassParticipant& firstParticipant,
                                                    MyClassHelpers::MyClassParticipant& secondParticipant)
{
  m_firstParticipant.m_participant.performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant(m_firstParticipant.m_participant.m_firstParticipant.m_participant),
                                                                         MyClassHelpers::MyClassParticipant(m_firstParticipant.m_participant.m_secondParticipant.m_participant));
  m_secondParticipant.m_participant.performRecursiveParticipantProcessing(MyClassHelpers::MyClassParticipant(m_secondParticipant.m_participant.m_firstParticipant.m_participant),
                                                                          MyClassHelpers::MyClassParticipant(m_secondParticipant.m_participant.m_secondParticipant.m_participant));
}



/*
Line break before lists, no '(' aligning.
*/

// Line break before lists, no '(' aligning: Class definition.
class MyClassD
{
  public:
    MyClassD(MyClassD& firstParticipant, MyClassD& secondParticipant);
    MyClassD(
      MyClassHelpers::MyClassParticipant firstParticipant,
      MyClassHelpers::MyClassParticipant secondParticipant);

    void performRecursiveParticipantProcessing(MyClassD& firstParticipant, MyClassD&secondParticipant);
    void performRecursiveParticipantProcessing(
      MyClassHelpers::MyClassParticipant& firstParticipant,
      MyClassHelpers::MyClassParticipant& secondParticipant);

  private:
    MyClassHelpers::MyClassParticipant m_participant1;
    MyClassHelpers::MyClassParticipant m_participant2;
};


// Line break before lists, no '(' aligning: Constructor 1 definition.
MyClassD::MyClassD(MyClassD& firstParticipant, MyClassD& secondParticipant) :
  MyClassD(
    MyClassHelpers::MyClassParticipant(firstParticipant),
    MyClassHelpers::MyClassParticipant(secondParticipant))
{
}


// Line break before lists, no '(' aligning: Constructor 2 definition.
MyClassD:: MyClassD(
  MyClassHelpers::MyClassParticipant fistParticipant,
  MyClassHelpers::MyClassParticipant secondParticipant)
  : m_firstParticipant(m_firstParticipant), m_secondParticipant(secondParticipant)
{
}


// Line break before lists, no '(' aligning: Member function 1 definition.
void MyClassD::performRecursiveParticipantProcessing(MyClassD& firstParticipant, MyClassD&secondParticipant)
{
  m_firstParticipant.performRecursiveParticipantProcessing(
    m_firstParticipant.m_participant, m_secondParticipant.m_participant);
}


// Line break before lists, no '(' aligning: Member function 2 definition.
void MyClassD::performRecursiveParticipantProcessing(
  MyClassHelpers::MyClassParticipant& firstParticipant, MyClassHelpers::MyClassParticipant& secondParticipant)
{
  m_firstParticipant.m_participant.performRecursiveParticipantProcessing(
    MyClassHelpers::MyClassParticipant(
      m_firstParticipant.m_participant.m_firstParticipant.m_participant),
    MyClassHelpers::MyClassParticipant(
      m_firstParticipant.m_participant.m_secondParticipant.m_participant));
  m_secondParticipant.m_participant.performRecursiveParticipantProcessing(
    MyClassHelpers::MyClassParticipant(
      m_secondParticipant.m_participant.m_firstParticipant.m_participant),
    MyClassHelpers::MyClassParticipant(
      m_secondParticipant.m_participant.m_secondParticipant.m_participant));
}
