Details of Extendible Hash:
  ●  We would be hashing on “TransactionID.”
  ●  Ideally, the buckets in the extendible hash should be stored in the secondary memory. However, for the purpose of this project, 
    they would be stored in something called “Simulated Secondary Memory.”
  ●  The directory or bucket address table of the extendible hash would contain the hash prefix and pointer to the bucket sitting in “Simulated Secondary Memory.”
  ●  “Main memory” can hold upto 1024 directory entries. The rest resides in your “SimulatedSecondary memory.”
  ●  The Least significant bits are extracted to find the directory entry.
  ●  Only one directory expansion is allowed per record insertion. Following the directory expansion, you may attemptto resolve the 
     collision (if it still persists) by increasing the local depth (if local depth < global depth). 
     In case thecollision is still not resolved, just create an overflow bucket
     
 Simulated Secondary Memory:
    #The secondary memory is simulated through an array of the abstract data-type “bucket”.
    #The bucket capacity is fixed in terms of number of records it can contain. 
    #Locations (indices) in this array form our “bucket address / hardware address.”
    #Here, the bucket abstract data-type would have the following information:
      a) Number of empty spaces.
      b) An array of structures to store the records. 
      c) Length of this array is fixed according to the parameter“bucket-size” specified.
      d) Link to the next bucket (valid only if this bucket is overflowing)
      e) All buckets in the overflow chain must be linked. 
      f) The last bucket of  the overflow chain must have aspecial character denoting that it is the end of the overflow chain.
