
/*
        Very long lines.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(myClass.m_firstParticipant, myClass.m_secondParticipant, myClass.weight * myClass.scale + myClass.offset);
}


/*
        Line break after first argument, not aligned with '('.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(myClass.m_firstParticipant,
		myClass.m_secondParticipant, myClass.weight * myClass.scale + myClass.offset);
}



/*
        Line break after '(', not aligned with '('.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(
		myClass.m_firstParticipant, myClass.m_secondParticipant, myClass.weight * myClass.scale + myClass.offset);
}


/*
        Line break after first argument, aligned with '('.
 */

void work(MyClass& myClass)
{
	myClass.performRecursiveParticipantProcessing(myClass.m_firstParticipant,
	                                              myClass.m_secondParticipant,
	                                              myClass.weight * myClass.scale + myClass.offset);
}
