import java.util.ArrayList;
import java.io.*;

public class spell_tezine{
	
	static boolean ne_pocinje_cifrom (String s){
		
	String [] niz = s.split(" ");
	
	char k = niz[0].charAt(0);
	
	if(k<'1' || k>'9')
		return true;
	else 
		return false;
	}
	


		
public static void main(String[]args){
	System.out.println("Ucitavanje u array list i mapiranje....");
	
	
	ArrayList <String> spisak_proteina  = new ArrayList<String>();
	ArrayList <String> biogrid_grane = new ArrayList<String>();
	
	
	try{
			BufferedReader br = new BufferedReader(new FileReader("biogridProteinsFilter.txt"));
			String line;
			boolean eof = false;
			while(!eof){
				line = br.readLine();
				if(line==null)
					eof = true;
				else{
					spisak_proteina.add(line);
			
				
				}
				
			}
			
			br.close();
		}
		catch(IOException e){
			System.out.println(e.toString());

		}
		
		
		try{
			BufferedReader br = new BufferedReader(new FileReader("BioGRID_final_reduced.txt"));
			String line;
			boolean eof = false;
			while(!eof){
				line = br.readLine();
				if(line==null)
					eof = true;
				else{
					biogrid_grane.add(line);
				}
				
			}
			
			br.close();
		}
		catch(IOException e){
			System.out.println(e.toString());

		}
		
				
			ArrayList <String> grane_tezine  = new ArrayList<String>();
			
		for(int i = 0; i< spisak_proteina.size();i++){
			
			String protein = spisak_proteina.get(i);
			
			try{
			BufferedReader br = new BufferedReader(new FileReader(protein+".txt"));
			String line;
			boolean eof = false;
			while(!eof){
				line = br.readLine();
				if(line==null)
					eof = true;
				else{
					
					
					
					if(line.compareTo("")==0 || ne_pocinje_cifrom(line))
					continue;
					
					else{
					
					
					String [] niz = line.split("\t");
					String drugi_protein = niz [1];
					
					if(spisak_proteina.contains(drugi_protein)&& (biogrid_grane.contains(protein+" "+drugi_protein) || biogrid_grane.contains(drugi_protein+" "+protein)))
					{
						String t = niz [3];
						String upis = protein+"\t"+drugi_protein+"\t"+t;
						String obrnut = drugi_protein+"\t"+protein+"\t"+t;
						if(!grane_tezine.contains(upis) && !grane_tezine.contains(obrnut))
						grane_tezine.add(upis);
					
						}					
					
					
					}
			
				
				}
				
			}
			
			br.close();
		}
		catch(IOException e){
			System.out.println(e.toString());

		}
		
		if(i%100 == 0)		
			System.out.println("Zavresno "+(i+1)+" datoteka");
		
	//	if(i==1)
	//	 break;
			
	}
		
		try{
			BufferedWriter bw = new BufferedWriter(new FileWriter("biogridReduced_weight.txt"));
			
			for(int a=0;a<grane_tezine.size();a++){
			bw.write(grane_tezine.get(a));
			bw.newLine();
	}

			bw.close();


	}catch(IOException e){
		System.out.println(e.toString());
	}
	
	

}
}